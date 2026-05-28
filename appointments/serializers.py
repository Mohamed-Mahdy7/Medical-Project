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
        read_only_fields = ["id", "created_at", "updated_at", "status"]

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
                f"The doctor is not available on this day. "
                f"Available days are based on the doctor's schedule."
            )

        slot_start = start_time.time()
        slot_end = end_time.time()
        avail_start = availability.start_time.time()
        avail_end = availability.end_time.time()

        if slot_start < avail_start or slot_end > avail_end:
            raise serializers.ValidationError(
                f"The selected slot is outside the doctor's available hours. "
                f"Available hours are {avail_start.strftime('%I:%M %p')} - "
                f"{avail_end.strftime('%I:%M %p')}."
            )
        
        expected_duration = timedelta(minutes=availability.slot_duration_minutes)
        actual_duration   = end_time - start_time

        if actual_duration != expected_duration:
            raise serializers.ValidationError(
                f"Appointment duration must be exactly {availability.slot_duration_minutes} minutes."
            )

        return attrs
        
    def create(self, validated_data):
        request = self.context.get("request")
        patient = request.user.patient_profile

        return Appointment.objects.create(patient=patient, **validated_data)


class AppointmentPatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status"]

    def validate_status(self, value):
        if value != Appointment.Status.CANCELLED:
            raise serializers.ValidationError("Patient can only cancel appointments")
        return value

    def validate(self, attrs):
        if self.instance.status != Appointment.Status.PENDING:
            raise serializers.ValidationError(
                f"Cannot cancel an appointment with status '{self.instance.status}'."
            )
        return attrs


class AppointmentDoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status", "notes"]

    def validate_status(self, value):
        if value == Appointment.Status.PENDING:
            raise serializers.ValidationError(
                "Doctors cannot set appointment status back to pending."
            )
        return value

    def validate(self, attrs):
        if self.instance.status in [Appointment.Status.COMPLETED, Appointment.Status.CANCELLED]:
            raise serializers.ValidationError(
                f"Cannot modify an appointment with status '{self.instance.status}'."
            )
        return attrs