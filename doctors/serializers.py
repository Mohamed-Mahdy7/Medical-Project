from rest_framework import serializers
from .models import (
    Specialty, DoctorProfile
)
from appointments.models import Appointment

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model=Specialty
        fields = [
            'id',
            'name',
            'description'
        ]


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'user',
            'specialty',
            'bio',
            'phone',
            'profile_picture',
            'years_of_experience'
        ]
class DoctorprofileappointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'status',
            'start_time',
            'end_time',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status']