from django.db import models
from django.conf import settings

# Create your models here.
class Patient(models.Model):

    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='patient_profile'
    )
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    medical_history_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile - {self.user.username}"