from rest_framework import serializers
from .models import PatientProfile
from datetime import date


class PatientProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = PatientProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
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