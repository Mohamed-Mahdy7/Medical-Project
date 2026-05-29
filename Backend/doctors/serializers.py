from rest_framework import serializers
from .models import (
    Specialty, DoctorProfile
)


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
