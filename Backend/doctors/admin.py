from django.contrib import admin
from .models import Specialty, DoctorProfile
from django.contrib import admin
from .models import DoctorProfile, Specialty


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    def created_at(self, obj):
        return obj.user.created_at
    
    list_display = [
        'id',
        'user',
        'specialty',
        'phone',
        'years_of_experience',
    ]

    list_filter = [
        'user__is_approved',
        'user__is_blocked',
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
    ]

    autocomplete_fields = ['specialty']