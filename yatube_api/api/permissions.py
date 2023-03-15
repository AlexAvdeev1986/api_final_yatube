from rest_framework import permissions


class IsAuthorOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Класс разрешений объект меняет только автор
    Доступ на чтение есть только у аунтефицированных пользователей
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Метод проверки доступа на уровне объекта"""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
