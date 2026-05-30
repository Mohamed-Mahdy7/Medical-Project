from rest_framework import serializers
from .models import PatientProfile
from datetime import date


class PatientProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientProfile
        fields = [
            'id',
            'date_of_birth',
            'gender',
            'phone',
            'address',
            'medical_history_notes',
        ]

    def validate_date_of_birth(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value