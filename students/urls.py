from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, StudentListView, StudentDetailView

urlpatterns = [
    path('list/', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]