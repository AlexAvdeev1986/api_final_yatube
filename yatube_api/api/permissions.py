from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """Чтение все. Измнения только авторизованные пользователи"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Чтение все. Изменения только авторы."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
