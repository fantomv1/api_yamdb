from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешает доступ только для админа."""

    def has_permission(self, request, view):
        """Разрешить доступ только для админа."""
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает доступ для админа или только для чтения."""

    def has_permission(self, request, view):
        """Разрешить доступ для админа или только для чтения."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    """Разрешает доступ для автора/модератора/админа или только для чтения."""

    def has_object_permission(self, request, view, obj):
        """Разрешить доступ для автора/модера/админа или только для чтения."""
        return request.method in permissions.SAFE_METHODS or (
            (request.user.is_authenticated and obj.author == request.user)
            or (
                request.user.is_authenticated
                and (request.user.is_moder or request.user.is_admin)
            )
        )
