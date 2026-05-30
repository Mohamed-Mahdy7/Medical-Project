from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPatient(BasePermission):
    message = "Only patients can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "P"


class IsDoctor(BasePermission):
    message = "Only doctors can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "D"
    

class IsAppointmentOwnerPatient(BasePermission):
    message = "You can only access your own appointments."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "P"

    def has_object_permission(self, request, view, obj):
        return obj.patient.user == request.user


class IsAppointmentOwnerDoctor(BasePermission):
    message = "You can only access your own appointments."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "D"

    def has_object_permission(self, request, view, obj):
        return obj.doctor.user == request.user


class CanModifyAppointment(BasePermission):
    message = "You do not have permission to modify this appointment."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True

        if user.role == "P":
            return obj.patient.user == user and obj.status == "PENDING"

        if user.role == "D":
            return obj.doctor.user == user

        return False