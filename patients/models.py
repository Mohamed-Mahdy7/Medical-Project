from django.db import models

# Create your models here.
class Patient(models.Model):
    date_of_birth = models.DateField(null=True)
    gender = models.BooleanField(null=True)
    phone = models.CharField(max_length=255)
    address = models.CharField()
    medical_history_notes = models.CharField()