from django.urls import path
from .views import CourseListView, CourseCreateUpdateView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('create/', CourseCreateUpdateView.as_view(), name='course-create'),
    path('<int:pk>/update/', CourseCreateUpdateView.as_view(), name='course-update'),
]