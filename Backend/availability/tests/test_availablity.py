import pytest
from datetime import time, timedelta
from django.utils import timezone
from availability.models import Availability
from appointments.models import Appointment


AVAIL_URL = "/availability/availability/"


@pytest.mark.django_db
class TestAvailabilityCRUD:

    def test_doctor_can_create_availability(self, doctor_client, doctor_profile):
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 1,
            "start_time": "09:00",
            "end_time": "12:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 201

    def test_patient_cannot_create_availability(self, patient_client):
        res = patient_client.post(AVAIL_URL, {
            "day_of_week": 1,
            "start_time": "09:00",
            "end_time": "12:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 403

    def test_unauthenticated_cannot_create(self, anon_client):
        res = anon_client.post(AVAIL_URL, {
            "day_of_week": 1,
            "start_time": "09:00",
            "end_time": "12:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 401

    def test_doctor_can_update_own_availability(self, doctor_client, availability):
        res = doctor_client.patch(
            f"{AVAIL_URL}{availability.pk}/", {"price": 300}
        )
        assert res.status_code == 200

    def test_doctor_can_delete_unbooked_availability(self, doctor_client, availability):
        res = doctor_client.delete(f"{AVAIL_URL}{availability.pk}/")
        assert res.status_code == 204

    def test_cannot_delete_booked_availability(
        self, doctor_client, availability, patient_profile, doctor_profile, monday
    ):
        start = timezone.make_aware(timezone.datetime.combine(monday, time(9, 0)))
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.PENDING,
        )
        res = doctor_client.delete(f"{AVAIL_URL}{availability.pk}/")
        assert res.status_code == 400

    def test_cannot_update_booked_availability(
        self, doctor_client, availability, patient_profile, doctor_profile, monday
    ):
        start = timezone.make_aware(timezone.datetime.combine(monday, time(9, 0)))
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.PENDING,
        )
        res = doctor_client.patch(f"{AVAIL_URL}{availability.pk}/", {"price": 500})
        assert res.status_code == 400


@pytest.mark.django_db
class TestAvailabilityOverlapValidation:

    def test_overlapping_slot_rejected(self, doctor_client, availability):
        # availability is Mon 09:00–11:00; this overlaps it
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 0,
            "start_time": "10:00",
            "end_time": "13:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 400

    def test_adjacent_slot_allowed(self, doctor_client, availability):
        # availability ends at 11:00; this starts at 11:00 — no overlap
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 0,
            "start_time": "11:00",
            "end_time": "13:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 201

    def test_different_day_no_overlap(self, doctor_client, availability):
        # Same hours, but Tuesday — should be fine
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 1,
            "start_time": "09:00",
            "end_time": "11:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 201

    def test_start_time_after_end_time_rejected(self, doctor_client):
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 2,
            "start_time": "13:00",
            "end_time": "09:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 400

    def test_start_equals_end_rejected(self, doctor_client):
        res = doctor_client.post(AVAIL_URL, {
            "day_of_week": 2,
            "start_time": "10:00",
            "end_time": "10:00",
            "slot_duration_minutes": 30,
            "price": 200,
        })
        assert res.status_code == 400