from rest_framework import serializers
from .models import Availability, DoctorProfile

class AvailabilitySerializer(serializers.Serializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset = DoctorProfile.objects.all())
    day_of_week = serializers.ChoiceField(choices=Availability.DayOfWeek.choices)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    slot_duration_minutes = serializers.IntegerField(min_value = 1)
    is_active = serializers.BooleanField(default=True)

def create(self, validated_data):
    return Availability.objects.create(**validated_data)

def update(self, instance, validated_data):

    instance.doctor = validated_data.get(
        'doctor',
        instance.doctor
    )

    instance.day_of_week = validated_data.get(
        'day_of_week',
        instance.day_of_week
    )

    instance.start_time = validated_data.get(
        'start_time',
        instance.start_time
    )

    instance.end_time = validated_data.get(
        'end_time',
        instance.end_time
    )

    instance.slot_duration_minutes = validated_data.get(
        'slot_duration_minutes',
        instance.slot_duration_minutes
    )

    instance.is_active = validated_data.get(
        'is_active',
        instance.is_active
    )

    instance.save()

    return instance