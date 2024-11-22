from django.urls import path
from .views import AttendanceListView, AttendanceUpdateView

urlpatterns = [
    path('', AttendanceListView.as_view(), name='attendance-list'),
    path('<int:pk>/', AttendanceUpdateView.as_view(), name='attendance-detail'),
]