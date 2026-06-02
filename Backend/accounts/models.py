from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        DOCTOR="D", "DOCTOR"
        PATIENT="P", "PATIENT"
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=10, choices=Roles.choices, null=False)
    is_approved = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"