from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated

from .serializers import AppointmentSerializer

class AppointmentViewSet(ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == user.Roles.DOCTOR:
            return Appointment.objects.filter(doctor=user)
        elif user.role == user.Roles.PATIENT:
            return appointment.objects.filter(patient=user)

        return Appointment.objects.all()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)