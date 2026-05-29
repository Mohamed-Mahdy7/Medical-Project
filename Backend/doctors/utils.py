from datetime import datetime, timedelta
from Backend.appointments.models import Appointment
from Backend.availability.models import Availability


def generate_available_slots(doctor_id, date):
    doctor_id = int(doctor_id)
    day_of_week = date.weekday()

    availabilities = Availability.objects.filter(
        doctor_id=doctor_id,
        day_of_week=day_of_week,
        is_active=True
    )

    if not availabilities.exists():
        return []

    # start_time is a DateTimeField — filter by date component
    booked_times = set(
        Appointment.objects.filter(
            doctor_id=doctor_id,
            start_time__date=date,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED]
        ).values_list('start_time', flat=True)
    )

    # booked_times contains full datetime objects — extract just the time
    booked_times = {dt.time().replace(second=0, microsecond=0) for dt in booked_times}

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

    