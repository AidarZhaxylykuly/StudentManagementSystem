from django.urls import path
from analytics.views import MostActiveUsersView, PopularCoursesView

urlpatterns = [
    path('most-active-users/', MostActiveUsersView.as_view(), name='most-active-users'),
    path('popular-courses/', PopularCoursesView.as_view(), name='popular-courses'),
]