from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import User

class IsAdminOrDoctorOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    if request.user.is_superuser or request.user.is_staff:
      return True

    elif request.user.role == User.Role.DOCTOR:
      if request.method == 'DELETE':
        return False
      return True

    return request.method in SAFE_METHODS
  