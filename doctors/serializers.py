from rest_framework import serializers

from .models import (
    Specialty,
    DoctorProfile
)


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:

        model = Specialty

        fields = '__all__'


class DoctorListSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    specialty = serializers.CharField(
        source='specialty.name',
        read_only=True
    )

    class Meta:

        model = DoctorProfile

        fields = [
            'id',
            'full_name',
            'email',
            'specialty',
            'years_of_experience',
            'profile_picture'
        ]


class DoctorDetailSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    specialty = SpecialtySerializer(
        read_only=True
    )

    class Meta:

        model = DoctorProfile

        fields = [
            'id',
            'full_name',
            'email',
            'specialty',
            'bio',
            'phone',
            'profile_picture',
            'years_of_experience',
            'is_approved',
            'is_blocked',
            'created_at'
        ]


class DoctorCreateUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = DoctorProfile

        fields = [
            'specialty',
            'bio',
            'phone',
            'profile_picture',
            'years_of_experience'
        ]

    def validate_phone(self, value):

        if len(value) != 11:

            raise serializers.ValidationError(
                'Phone must be 11 digits'
            )

        return value