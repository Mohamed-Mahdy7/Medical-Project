from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from patients.models import Patient

from doctors.models import DoctorProfile

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
    )
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appointments"
        verbose_name = "Appointment"
        verbose_name_plural= "Appointments"

        ordering = ["start_time"]

        indexes = [
            models.Index(fields=["patient"], name="patient_appointment_index"),
            models.Index(fields=["doctor", "status"], name="appointment_doctor_status_idx"),
            models.Index(fields=["patient", "status"], name="appointment_patient_status_idx"),
            models.Index(fields=["start_time"], name="appointment_start_time_index"),
        ]

        constraints = [
            # Prevent double booking: same doctor can't have two non-cancelled appointments at the same time
            models.UniqueConstraint(
                fields=["doctor", "start_time"],
                condition = ~models.Q(status="CANCELLED"),
                name="unique_doctor_appointment_time"
            )
        ]

    def clean(self):
        # end_time must always be after start_time
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("end_time must be after start_time.")

        # Only check past time on new appointments, not on updating old ones (e.g. changing status from confirmed to completed)
        if self.start_time and self.start_time < timezone.now() and not self.pk:
            raise ValidationError("Appointment cannot be booked in the past.")

        # Prevent overlapping appointments for the same doctor
        if self.start_time and self.end_time and self.doctor_id:
            overlapping = Appointment.objects.filter(
                doctor_id=self.doctor_id,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(status=Appointment.Status.CANCELLED)

            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            
            if overlapping.exists():
                raise ValidationError(
                    "This doctor already has an appointment at this time"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} -> {self.doctor} | {self.start_time}"
