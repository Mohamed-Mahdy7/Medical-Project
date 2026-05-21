from django.utils import timezone

from rest_framework import serializers

from .models import Appointment

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["doctor", "start_time", "end_time"]

    def validate(self, attrs):
        doctor = attrs.get("doctor")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        request = self.context.get("request")

    if start_time < timezone.now():
        raise serializers.ValidationError("Appointment cannot be booked in the past.")

    if end_time <= start_time:
        raise serializers.ValidationError("end_time must be after start_time.")