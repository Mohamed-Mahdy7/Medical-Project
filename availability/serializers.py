from rest_framework import serializers
from .models import Availability, DoctorProfile

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'slot_duration_minutes', 'is_active']
        read_only_fields = ['id']

    def validate(self, data):
        request = self.context.get('request')
        doctor = request.user.doctorprofile

        start = data.get('start_time', getattr(self.instance, 'start_time', None))
        end = data.get('end_time', getattr(self.instance, 'end_time', None))
        day = data.get('day_of_week', getattr(self.instance, 'day_of_week', None))

        if start >= end:
            raise serializers.ValidationError("Start time must be before end time.")

        qs = Availability.objects.filter(
            doctor=doctor,
            day_of_week=day,
            start_time__lt=end,
            end_time__gt=start
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "This overlaps with an existing availability slot."
            )

        return data

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user.doctorprofile
        return Availability.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('doctor', None)  
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance