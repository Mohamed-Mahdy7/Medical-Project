from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    AppointmentDetailSerializer,
    AppointmentCreateSerializer,
    AppointmentPatientUpdateSerializer,
    AppointmentDoctorUpdateSerializer,
)
from .permissions import (
    IsPatient,
    CanModifyAppointment,
)
from .models import Appointment


class AppointmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_base_queryset(self):
        return Appointment.objects.select_related(
            "patient__user", "doctor__user", "doctor__specialty"
        )

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return self.get_base_queryset().all()

        if user.role == "P":
            return self.get_base_queryset().filter(patient=user.patient_profile)

        if user.role == "D":
            return self.get_base_queryset().filter(doctor=user.doctor_profile)

        return Appointment.objects.none()

    def get_permissions(self):
        if self.action == "create":
            return [IsPatient()]

        if self.action in ["update", "partial_update"]:
            return [CanModifyAppointment()]

        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer

        if self.action in ["update", "partial_update"]:
            user = self.request.user

            if user.role == "P":
                return AppointmentPatientUpdateSerializer

            if user.role == "D":
                return AppointmentDoctorUpdateSerializer
            return AppointmentDetailSerializer

        return AppointmentDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                "status": "error",
                "message": "Appointments cannot be deleted. Please cancel instead.",
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )