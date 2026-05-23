from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from .models import Appointment
from availability.models import Availability

class AppointmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Appointment
        fields = [
            "id",
            "doctor",
            "patient",
            "status",
            "start_time",
            "end_time",
            "notes",
            "created_at",
            "updated_at",
        ]

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

        day_of_week = start_time.weekday()

        availability = Availability.objects.filter(
            doctor=doctor,
            day_of_week=day_of_week,
            is_active=True,
        ).first()

        if not availability:
            raise serializers.ValidationError(
                "The doctor is not available on this day."
            )

        slot_start = start_time.time()
        slot_end = end_time.time()
        avail_start = availability.start_time.time()
        avail_end = availability.end_time.time()

        if slot_start < avail_start or slot_end > avail_end:
            raise serializers.ValidationError(
                "The selected slot is outside the doctor's available hours."
            )

        return attrs
        
