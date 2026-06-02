import pytest
from datetime import time, timedelta
from django.utils import timezone
from doctors.models import DoctorProfile, Specialty
from doctors.utils import generate_available_slots
from appointments.models import Appointment


DOCTORS_URL   = "/doctors/"
SPECIALTY_URL = "/doctors/specialties/"


@pytest.mark.django_db
class TestSpecialty:

    def test_admin_can_create_specialty(self, admin_client):
        res = admin_client.post(SPECIALTY_URL, {"name": "Neurology", "description": "Brain"})
        assert res.status_code == 201

    def test_patient_cannot_create_specialty(self, patient_client):
        res = patient_client.post(SPECIALTY_URL, {"name": "Neurology", "description": "Brain"})
        assert res.status_code == 403

    def test_list_specialties_public(self, anon_client, specialty):
        res = anon_client.get(SPECIALTY_URL)
        assert res.status_code == 200

    def test_duplicate_specialty_name_rejected(self, admin_client, specialty):
        res = admin_client.post(SPECIALTY_URL, {"name": specialty.name})
        assert res.status_code == 400


@pytest.mark.django_db
class TestDoctorProfile:

    def test_list_doctors_authenticated(self, patient_client, doctor_profile):
        res = patient_client.get(DOCTORS_URL)
        assert res.status_code == 200

    def test_list_doctors_unauthenticated(self, anon_client):
        res = anon_client.get(DOCTORS_URL)
        assert res.status_code == 401

    def test_doctor_profile_includes_available_slots(self, patient_client, doctor_profile):
        res = patient_client.get(f"{DOCTORS_URL}{doctor_profile.pk}/")
        assert res.status_code == 200
        assert "available_slots" in res.data

    def test_slots_endpoint_requires_date_param(self, patient_client, doctor_profile):
        res = patient_client.get(f"{DOCTORS_URL}{doctor_profile.pk}/slots/")
        assert res.status_code == 400

    def test_slots_endpoint_rejects_invalid_date(self, patient_client, doctor_profile):
        res = patient_client.get(f"{DOCTORS_URL}{doctor_profile.pk}/slots/?date=not-a-date")
        assert res.status_code == 400

    def test_slots_endpoint_rejects_past_date(self, patient_client, doctor_profile):
        yesterday = (timezone.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        res = patient_client.get(f"{DOCTORS_URL}{doctor_profile.pk}/slots/?date={yesterday}")
        assert res.status_code == 400

    def test_slots_returned_for_valid_date(self, patient_client, doctor_profile, availability, monday):
        res = patient_client.get(
            f"{DOCTORS_URL}{doctor_profile.pk}/slots/?date={monday.strftime('%Y-%m-%d')}"
        )
        assert res.status_code == 200
        assert "available_slots" in res.data["data"]
        assert len(res.data["data"]["available_slots"]) > 0

    def test_no_slots_when_no_availability(self, patient_client, doctor_profile, monday):
        # No availability created for this doctor
        res = patient_client.get(
            f"{DOCTORS_URL}{doctor_profile.pk}/slots/?date={monday.strftime('%Y-%m-%d')}"
        )
        assert res.status_code == 200
        assert res.data["data"]["available_slots"] == []


@pytest.mark.django_db
class TestGenerateAvailableSlots:
    """Unit tests for the generate_available_slots utility directly."""

    def test_returns_correct_slot_count(self, doctor_profile, availability, monday):
        # 09:00–11:00 with 30-min slots = 4 slots
        slots, duration = generate_available_slots(doctor_profile.pk, monday)
        assert len(slots) == 4
        assert duration == 30

    def test_booked_slot_excluded(self, doctor_profile, patient_profile, availability, monday):
        start = timezone.make_aware(timezone.datetime.combine(monday, time(9, 0)))
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.PENDING,
        )
        slots, _ = generate_available_slots(doctor_profile.pk, monday)
        slot_times = [s[1] for s in slots]
        assert "09:00" not in slot_times
        assert len(slots) == 3

    def test_cancelled_appointment_slot_still_available(
        self, doctor_profile, patient_profile, availability, monday
    ):
        start = timezone.make_aware(timezone.datetime.combine(monday, time(9, 0)))
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.CANCELLED,
        )
        slots, _ = generate_available_slots(doctor_profile.pk, monday)
        slot_times = [s[1] for s in slots]
        assert "09:00" in slot_times

    def test_no_availability_returns_empty(self, doctor_profile, monday):
        slots, duration = generate_available_slots(doctor_profile.pk, monday)
        assert slots == []
        assert duration is None

    def test_fully_booked_returns_empty(
        self, doctor_profile, patient_profile, availability, monday
    ):
        for hour, minute in [(9, 0), (9, 30), (10, 0), (10, 30)]:
            start = timezone.make_aware(
                timezone.datetime.combine(monday, time(hour, minute))
            )
            Appointment.objects.create(
                patient=patient_profile,
                doctor=doctor_profile,
                availability=availability,
                start_time=start,
                end_time=start + timedelta(minutes=30),
                status=Appointment.Status.PENDING,
            )
        slots, _ = generate_available_slots(doctor_profile.pk, monday)
        assert slots == []

    def test_wrong_day_returns_empty(self, doctor_profile, availability):
        # availability is Monday (0), pass Tuesday
        tuesday = next_weekday(1)
        slots, duration = generate_available_slots(doctor_profile.pk, tuesday)
        assert slots == []
        assert duration is None


def next_weekday(weekday):
    from datetime import date, timedelta as td
    today = date.today()
    days_ahead = (weekday - today.weekday()) % 7 or 7
    return today + td(days=days_ahead)