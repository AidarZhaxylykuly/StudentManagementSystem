from rest_framework import viewsets, generics
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from students.permissions import IsStudent, IsTeacher, IsAdmin
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from drf_yasg.utils import swagger_auto_schema
from analytics.utils import send_to_google_analytics


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List of all students",
        responses={200: StudentSerializer(many=True)}
    )
    def get_permissions(self):
        if self.request.user.role == 'TC':
            return [IsAuthenticated, IsTeacher()]
        elif self.request.user.role == 'AD':
            return [IsAuthenticated, IsAdmin()]
        else:
            return [IsAuthenticated, IsStudent()]

    def perform_create(self, serializer):
        student = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint='/students/create')
        cache.delete('all_students')

    def perform_update(self, serializer):
        student = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint=f'/students/{student.id}/update')
        cache.delete('all_students')

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        send_to_google_analytics(user_id=self.request.user.id, endpoint=f'/students/{instance.id}/delete')
        cache.delete('all_students')


class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all students or create a new student",
        responses={200: StudentSerializer(many=True)},
        request_body=StudentSerializer,
    )
    def get_queryset(self):
        cache_key = 'all_students'
        log_cache_hit_miss(cache_key)
        students = cache.get(cache_key)

        if not students:
            students = Student.objects.all()
            cache.set(cache_key, students, timeout=3600)

        return students

    def list(self, request, *args, **kwargs):
        send_to_google_analytics(user_id=request.user.id, endpoint='/students/list')
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new student",
        responses={201: StudentSerializer},
    )
    def perform_create(self, serializer):
        student = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint='/students/create')
        cache.delete('all_students')


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of a student",
        responses={200: StudentSerializer},
    )
    def get(self, request, *args, **kwargs):
        send_to_google_analytics(user_id=request.user.id, endpoint=f'/students/{kwargs["pk"]}/retrieve')
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update details of an existing student",
        responses={200: StudentSerializer},
        request_body=StudentSerializer,
    )
    def perform_update(self, serializer):
        student = serializer.save()
        send_to_google_analytics(user_id=self.request.user.id, endpoint=f'/students/{student.id}/update')
        cache.delete('all_students')

    @swagger_auto_schema(
        operation_description="Delete a student",
        responses={204: 'No Content'},
    )
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        send_to_google_analytics(user_id=self.request.user.id, endpoint=f'/students/{instance.id}/delete')
        cache.delete('all_students')


@receiver(post_save, sender=Student)
def clear_student_cache(sender, instance, **kwargs):
    cache.delete('all_students')


@receiver(post_delete, sender=Student)
def clear_student_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_students')