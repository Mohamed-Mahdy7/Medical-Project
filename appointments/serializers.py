from django.utils import timezone

from rest_framework import serializers

from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    read_only_fields = (
        "patient",
        "status",
        "create_at",
        "updated_at",
    )

    def update(self, instance, validated_data):
        validated_data.pop("patient", None)
        validated_data.pop("doctor", None)

        return super().update(instance, validated_data)

    def validate_appoientment_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Appointment cannot be in the past.")

        return value

    def validate(self, attrs):
        doctor = attrs.get("doctor")

        appointment_date = attrs.get("appointment_date")

        if doctor.role != doctor.Roles.DOCTOR:
            raise serializers.ValidationError({
                "doctor": "Selected user is not a doctor."
            })

        queryset = Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "appointment_date": "Doctor already has an appointment at this time."
            })

        return attrs
