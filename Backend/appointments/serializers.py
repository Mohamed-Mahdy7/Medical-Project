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

class AppointmentRescheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["start_time"]

    def validate(self, attrs):
        new_start_time = attrs.get("start_time")
        instance = self.instance
        request = self.context.get("request")

        if new_start_time < timezone.now():
            raise serializers.ValidationError("Cannot reschedule to a past time.")

        if instance.status not in [
            Appointment.Status.PENDING,
            Appointment.Status.CONFIRMED
        ]:
            raise serializers.ValidationError(
                f"Cannot reschedule an appointment with status '{instance.status}'."
            )

        # Find the availability window covering the new start_time
        availability = Availability.objects.filter(
            doctor=instance.doctor,
            day_of_week=new_start_time.weekday(),
            start_time__lte=new_start_time.time(),
            end_time__gt=new_start_time.time(),
            is_active=True
        ).first()

        if not availability:
            raise serializers.ValidationError(
                "The requested time is outside the doctor's availability."
            )

        # Check slot is free — exclude current appointment
        conflict = Appointment.objects.filter(
            doctor=instance.doctor,
            start_time=new_start_time,
        ).exclude(
            status=Appointment.Status.CANCELLED
        ).exclude(
            pk=instance.pk
        ).exists()

        if conflict:
            raise serializers.ValidationError("This slot is already booked.")

        # Store computed end_time for use in update()
        attrs['end_time'] = new_start_time + timedelta(
            minutes=availability.slot_duration_minutes
        )

        return attrs

    def update(self, instance, validated_data):
        instance.start_time = validated_data['start_time']
        instance.end_time = validated_data['end_time']
        instance.save()
        return instance