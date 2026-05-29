from django.db import models
from django.core.exceptions import ValidationError
from doctors.models import DoctorProfile

class Availability(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY    = 0, 'Monday'
        TUESDAY   = 1, 'Tuesday'
        WEDNESDAY = 2, 'Wednesday'
        THURSDAY  = 3, 'Thursday'
        FRIDAY    = 4, 'Friday'
        SATURDAY  = 5, 'Saturday'
        SUNDAY    = 6, 'Sunday'

    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'day_of_week', 'start_time', 'end_time'],
                name='unique_doctor_availability_slot'
            )
        ]

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Start time must be before end time.")

        qs = Availability.objects.filter(
            doctor=self.doctor,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                f"This overlaps with an existing availability slot on "
                f"{self.get_day_of_week_display()} "
                f"({self.start_time} - {self.end_time})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr.{self.doctor} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"