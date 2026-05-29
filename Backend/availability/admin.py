from django.contrib import admin
from .models import Availability

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):

    list_display = [
        "doctor",
        "day_of_week",
        "start_time",
        "end_time",
        "slot_duration_minutes",
        "is_active",
    ]

    list_filter = [
        "day_of_week",
        "is_active",
    ]

    search_fields = [
        "doctor__user__username",
    ]

    ordering = [
        "day_of_week",
        "start_time",
    ]

    list_editable = [
        "is_active",
    ]

    list_per_page = 10