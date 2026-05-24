from django.contrib import admin
from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['gender']