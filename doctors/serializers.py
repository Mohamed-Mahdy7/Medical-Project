from rest_framework import serializers

from .models import (
    Specialty,
    DoctorProfile
)

from appointments.models import (
    Appointment
)


class SpecialtySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Specialty

        fields = [
            'id',
            'name',
            'description'
        ]


class DoctorListSerializer(
    serializers.ModelSerializer
):

    full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    specialty_name = serializers.CharField(
        source='specialty.name',
        read_only=True
    )

    class Meta:

        model = DoctorProfile

        fields = [
            'id',
            'full_name',
            'specialty_name',
            'years_of_experience',
            'profile_picture'
        ]


class DoctorDetailSerializer(
    serializers.ModelSerializer
):

    specialty = SpecialtySerializer(
        read_only=True
    )

    full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:

        model = DoctorProfile

        fields = '__all__'


class DoctorUpdateSerializer(
    serializers.ModelSerializer
):

    specialty_id = serializers.PrimaryKeyRelatedField(

        queryset=Specialty.objects.all(),

        source='specialty'
    )

    class Meta:

        model = DoctorProfile

        fields = [

            'specialty_id',

            'bio',

            'phone',

            'profile_picture',

            'years_of_experience'
        ]

    def validate_phone(
        self,
        value
    ):

        if len(value) != 11:

            raise serializers.ValidationError(
                'Phone must be 11 digits'
            )

        return value


class DoctorAppointmentSerializer(
    serializers.ModelSerializer
):

    patient_name = serializers.CharField(

        source='patient.user.get_full_name',

        read_only=True
    )

    class Meta:

        model = Appointment

        fields = [

            'id',

            'patient_name',

            'date',

            'start_time',

            'end_time',

            'status',

            'note'
        ]