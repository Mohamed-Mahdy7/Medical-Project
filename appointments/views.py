from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated

from .serializers import (
    AppointmentDetailSerializer,
    AppointmentCreateSerializer
)
from .models import Appointment

class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Appointment.objects.select_related(
                "patient__user", "doctor__user", "doctor__specialty"
            ).all()

        if user.role == "P":
            return Appointment.objects.select_related(
                "patient__user", "doctor__user", "doctor__specialty"
            ).filter(patient=user.patient_profile)

        if user.role == "D":
            return Appointment.objects.select_related(
                "patient__user", "doctor__user", "doctor__specialty"
            ).filter(doctor=user.doctor_profile)

        return Appointment.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        return AppointmentDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
