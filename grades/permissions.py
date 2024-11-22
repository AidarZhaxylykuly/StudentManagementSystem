from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'TC'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ST'