from django.contrib import admin

from .models import Specialty, DoctorProfile

 
from django.contrib import admin
from .models import DoctorProfile, Specialty


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'specialty',
        'phone',
        'is_approved',
        'is_blocked',
        'years_of_experience',
        'created_at'
    ]

    list_filter = [
        'is_approved',
        'is_blocked',
        'specialty'
    ]

    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone'
    ]

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    autocomplete_fields = ['specialty']