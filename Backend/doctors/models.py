from django.db import models
from django.conf import settings


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctors'
    )

    bio = models.TextField(blank=True)

    phone = models.CharField(max_length=11)

    profile_picture = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )

    years_of_experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name() 
     
