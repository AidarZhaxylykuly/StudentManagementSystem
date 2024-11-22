from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from students.utils import log_cache_hit_miss
from drf_yasg.utils import swagger_auto_schema
from analytics.utils import send_to_google_analytics


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        operation_description="Get list of all courses",
        responses={200: CourseSerializer(many=True)}
    )
    def get_queryset(self):
        send_to_google_analytics(user_id=self.request.user.id, endpoint='/courses/list')
        cache_key = 'all_courses'

        log_cache_hit_miss(cache_key)

        courses = cache.get(cache_key)

        if not courses:
            courses = Course.objects.all()
            cache.set(cache_key, courses, timeout=3600)

        return courses


class CourseCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Create a new course",
        responses={201: CourseSerializer},
        request_body=CourseSerializer,
    )
    def perform_create(self, serializer):
        course = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint='/courses/create')
        cache.delete('all_courses')

    @swagger_auto_schema(
        operation_description="Update an existing course",
        responses={200: CourseSerializer},
        request_body=CourseSerializer,
    )
    def perform_update(self, serializer):
        course = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint=f'/courses/{course.id}/update')
        cache.delete('all_courses')


@receiver(post_save, sender=Course)
def clear_course_cache(sender, instance, **kwargs):
    cache.delete('all_courses')
    send_to_google_analytics(user_id=instance.updated_by.id, endpoint=f'/courses/{instance.id}/cache_clear')
