from rest_framework.permissions import BasePermission, SAFE_METHODS

class AppointmentPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return user.role == user.Roles.PATIENT

        return user.role == user.Roles.DOCTOR