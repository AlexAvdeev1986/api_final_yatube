from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """Чтение все. Измнения только авторизованные пользователи"""
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Чтение все. Изменения только авторы."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
