from django.urls import path
from .views import GradeListView, GradeUpdateView

urlpatterns = [
    path('', GradeListView.as_view(), name='grade-list'),
    path('<int:pk>/', GradeUpdateView.as_view(), name='grade-detail'),
]