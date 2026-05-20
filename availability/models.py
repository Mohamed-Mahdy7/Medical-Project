from django.db import models
from doctors.models import Doctor
# Create your models here.
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
        Doctor, on_delete = models.CASCADE
    )
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    slot_duration_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"Dr.{self.doctor} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"