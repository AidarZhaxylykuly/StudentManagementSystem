from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from courses.models import Course
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


class CourseAPITest(APITestCase):
    def setUp(self):
        self.course_data = {"name": "Physics", "description": "Learn basic physics"}

    def test_create_course(self):
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_courses(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class RoleBasedPermissionTestCase(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="password123", is_staff=True)
        self.student = User.objects.create_user(username="student", password="password123", is_staff=False)

        self.course = Course.objects.create(title="Math 101", description="Basic Math Course")

        self.course_url = reverse('course-detail', args=[self.course.id])

    def test_teacher_can_edit_course(self):
        self.client.login(username="teacher", password="password123")

        response = self.client.patch(self.course_url, {"title": "Advanced Math 101"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Advanced Math 101")

    def test_student_cannot_edit_course(self):
        self.client.login(username="student", password="password123")

        response = self.client.patch(self.course_url, {"title": "Unauthorized Update"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_course(self):
        self.client.login(username="student", password="password123")

        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseCacheTestCase(TestCase):

    def setUp(self):
        self.course = Course.objects.create(title="Math 101", description="Basic Math Course")
        self.cache_key = f"course_{self.course.id}"

    def test_cache_set_and_get(self):
        cache.set(self.cache_key, self.course, timeout=60)

        cached_course = cache.get(self.cache_key)
        self.assertEqual(cached_course, self.course)

    def test_cache_is_used_on_subsequent_requests(self):
        cache.set(self.cache_key, self.course, timeout=60)

        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['title'], self.course.title)
        self.assertEqual(response.data['description'], self.course.description)

    def test_cache_miss_when_not_set(self):
        cached_course = cache.get(self.cache_key)
        self.assertIsNone(cached_course)

        response = self.client.get(reverse('course-detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cached_course = cache.get(self.cache_key)
        self.assertIsNotNone(cached_course)
        self.assertEqual(cached_course.title, self.course.title)
        self.assertEqual(cached_course.description, self.course.description)

    def test_cache_expiration(self):
        cache.set(self.cache_key, self.course, timeout=2)

        cached_course = cache.get(self.cache_key)
        self.assertEqual(cached_course, self.course)

        import time
        time.sleep(3)

        cached_course = cache.get(self.cache_key)
        self.assertIsNone(cached_course)