from django.contrib import admin

from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient', 
        'doctor', 
        'status', 
        'start_time', 
        'end_time', 
        'created_at'
    ]

    list_filter = [
        'status', 
        'doctor__specialty'
    ]

    search_fields = [
        'patient__user__username', 
        'patient__user__email',
        'doctor__user__username', 
        'doctor__user__email'
    ]

    ordering = ['start_time']

    readonly_fields = ['id', 'created_at', 'updated_at']

admin.site.register(Appointment, AppointmentAdmin)