from rest_framework import serializers
from datetime import date
from .models import (
    Specialty, DoctorProfile
)
from .utils import generate_available_slots


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model=Specialty
        fields = [
            'id',
            'name',
            'description'
        ]


class DoctorProfileSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()
    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'user',
            'specialty',
            'bio',
            'phone',
            'profile_picture',
            'years_of_experience',
            'available_slots'
        ]

        def get_available_slots(self, obj):
            request = self.context.get('request')
            date_str = request.query_params.get('date') if request else None
    
            if date_str:
                from datetime import datetime
                try:
                    query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    return []
            else:
                query_date = date.today()
    
            return generate_available_slots(doctor_id=obj.pk, date=query_date)
