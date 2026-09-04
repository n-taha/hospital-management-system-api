from rest_framework.permissions import SAFE_METHODS, BasePermission

from ai import views


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user)


class IsAdminOrOwnerReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create",  "destroy"]:
            return request.user.is_authenticated and request.user.is_superuser
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_staff
        ):
            return True
        if request.method in ['PUT', 'PATCH']:
            return request.user == obj.user

class IsAdminCanDestroy(BasePermission):
    def has_permission(self, request, view):

        if view.action in ['list', 'retrieve', 'update', 'partial_update']:
            if request.user.is_authenticated:
                return True
            return False

        if view.action == 'destroy':
            if request.user.is_superuser or request.user.is_staff:
                return True
            return False

