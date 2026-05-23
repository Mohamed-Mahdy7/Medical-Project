from django.contrib import admin
from .models import Patient

# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['gender']