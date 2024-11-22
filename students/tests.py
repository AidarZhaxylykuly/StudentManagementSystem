from rest_framework.test import APITestCase
from rest_framework import status
from students.models import Student, Attendance
from courses.models import Course
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings

class StudentAPITest(APITestCase):
    def setUp(self):
        self.student_data = {
            "first_name": "Aidar",
            "last_name": "Zhaxylykuly",
            "email": "aidarzhaxylykuly@mail.com"
        }

    def test_create_student(self):
        response = self.client.post('/api/students/', self.student_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentPermissionsTestCase(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="password123", is_staff=True)
        self.student = User.objects.create_user(username="student", password="password123", is_staff=False)

        self.student_profile = Student.objects.create(user=self.student, enrolled=True)

        self.course = Course.objects.create(title="Math 101", description="Basic Math Course")

        self.attendance_url = reverse('attendance-list')
        self.grade_url = reverse('grade-list')

    def test_student_can_view_their_own_attendance(self):
        Attendance.objects.create(student=self.student_profile, course=self.course, attended=True)

        self.client.login(username="student", password="password123")

        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.title, [attendance['course'] for attendance in response.data])

    def test_student_cannot_view_others_attendance(self):
        another_student = User.objects.create_user(username="another_student", password="password123", is_staff=False)
        another_student_profile = Student.objects.create(user=another_student, enrolled=True)
        Attendance.objects.create(student=another_student_profile, course=self.course, attended=False)

        self.client.login(username="student", password="password123")

        response = self.client.get(self.attendance_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_their_grades(self):
        self.client.login(username="student", password="password123")

        response = self.client.get(self.grade_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course.title, [grade['course'] for grade in response.data])

    def test_student_cannot_view_others_grades(self):
        another_student = User.objects.create_user(username="another_student", password="password123", is_staff=False)
        another_student_profile = Student.objects.create(user=another_student, enrolled=True)

        self.client.login(username="student", password="password123")

        response = self.client.get(self.grade_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_update_their_profile(self):
        self.client.login(username="student", password="password123")

        response = self.client.patch(reverse('student-detail', args=[self.student_profile.id]),
                                     data={"enrolled": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_profile.refresh_from_db()
        self.assertFalse(self.student_profile.enrolled)

    def test_student_cannot_update_others_profile(self):
        another_student = User.objects.create_user(username="another_student", password="password123", is_staff=False)
        another_student_profile = Student.objects.create(user=another_student, enrolled=True)

        self.client.login(username="student", password="password123")

        response = self.client.patch(reverse('student-detail', args=[another_student_profile.id]),
                                     data={"enrolled": False})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CacheTestCase(APITestCase):

    def setUp(self):
        self.student = Student.objects.create(user__username='student', user__password='password123')
        self.course = Course.objects.create(title="Math 101", description="Basic Math Course")
        self.cache_key = f"student_{self.student.id}_courses"

    def test_cache_set_and_get(self):
        cache.set(self.cache_key, self.course, timeout=60)

        cached_course = cache.get(self.cache_key)
        self.assertEqual(cached_course, self.course)

    def test_cache_data_is_fetched_from_cache_on_subsequent_requests(self):
        cache.set(self.cache_key, self.course, timeout=60)

        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, cache.get(self.cache_key))

    def test_cache_miss(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, 200)

        cache.set(self.cache_key, self.course, timeout=60)
        cached_course = cache.get(self.cache_key)
        self.assertIsNotNone(cached_course)