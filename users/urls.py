from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet
from .views import UserRegisterView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('register/', UserRegisterView.as_view(), name='register'),
]