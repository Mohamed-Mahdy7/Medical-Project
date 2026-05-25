from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Availability
from .serializers import AvailabilitySerializer
from appointments.permissions import IsDoctor


class AvailabilityViewSet(ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsDoctor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "D":
            return Availability.objects.filter(doctor__user=user)

        return Availability.objects.all()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)