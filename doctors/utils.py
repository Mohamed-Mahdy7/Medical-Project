from datetime import datetime, timedelta
from appointments.models import Appointment
from availability.models import Availability


def generate_available_slots(doctor_id, date):
    day_of_week = date.weekday()  # 0=Monday ... 6=Sunday

    availabilities = Availability.objects.filter(
        doctor_id=doctor_id,
        day_of_week=day_of_week,
        is_active=True
    )

    if not availabilities.exists():
        return []

    booked_times = set(
        Appointment.objects.filter(
            doctor_id=doctor_id,
            date=date,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED]
        ).values_list('start_time', flat=True)
    )

    available_slots = []

    for availability in availabilities:
        slot_start = datetime.combine(date, availability.start_time)
        slot_end = datetime.combine(date, availability.end_time)
        delta = timedelta(minutes=availability.slot_duration_minutes)

        current = slot_start
        while current + delta <= slot_end:
            if current.time() not in booked_times:
                available_slots.append(current.time().strftime('%H:%M'))
            current += delta

    return available_slots