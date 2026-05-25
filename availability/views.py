from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Availability
from .serializers import AvailabilitySerializer
from appointments.permissions import IsDoctor
from rest_framework.exceptions import ValidationError


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
        self._validate_business_rules(serializer.validated_data)
        serializer.save(doctor=self.request.user.doctorprofile)

    def perform_update(self, serializer):
        self._validate_business_rules(serializer.validated_data)
        serializer.save()

    def _validate_business_rules(self, data):
            start = data['start_time']
            end = data['end_time']

            doctor = self.request.user.doctorprofile

            if start >= end:
                raise ValidationError("Start must be before end.")

            if start.date() != end.date():
                raise ValidationError("Start and end must be on the same day.")

            if start.weekday() != data['day_of_week']:
                raise ValidationError("Selected weekday does not match date.")

            if Availability.objects.filter(
                doctor=doctor,
                day_of_week=data['day_of_week'],
                start_time__lt=end,
                end_time__gt=start
            ).exists():
                raise ValidationError("Overlapping availability is not allowed.")