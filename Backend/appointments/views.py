from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


from .serializers import (
    AppointmentDetailSerializer,
    AppointmentCreateSerializer,
    AppointmentPatientUpdateSerializer,
    AppointmentDoctorUpdateSerializer,
    AppointmentRescheduleSerializer,
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
        from django.utils import timezone
        user = self.request.user

        if user.is_staff:
            queryset = self.get_base_queryset().all()
        elif user.role == "P":
            queryset = self.get_base_queryset().filter(patient=user.patient_profile)
        elif user.role == "D":
            queryset = self.get_base_queryset().filter(doctor=user.doctor_profile)
        else:
            return Appointment.objects.none()

        # Filter by status
        appointment_status = self.request.query_params.get('status')
        if appointment_status:
            queryset = queryset.filter(status=appointment_status)

        # Filter by type
        appointment_type = self.request.query_params.get('type')
        if appointment_type == 'upcoming':
            queryset = queryset.filter(start_time__gte=timezone.now())
        elif appointment_type == 'past':
            queryset = queryset.filter(start_time__lt=timezone.now())

        return queryset

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
    
    @action(detail=True, methods=['patch'], url_path='reschedule')
    def reschedule(self, request, pk=None):
        appointment = self.get_object()

        serializer = AppointmentRescheduleSerializer(
            appointment,
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Invalid data.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "status": "success",
            "message": "Appointment rescheduled successfully.",
            "data": AppointmentDetailSerializer(serializer.instance).data
        }, status=status.HTTP_200_OK)