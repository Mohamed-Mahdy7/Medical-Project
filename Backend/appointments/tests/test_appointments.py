import pytest
from datetime import time, timedelta
from django.utils import timezone
from appointments.models import Appointment


APPT_URL = "/appointments/"


def make_start(monday, h=9, m=0):
    return timezone.make_aware(timezone.datetime.combine(monday, time(h, m)))


@pytest.mark.django_db
class TestBookAppointment:

    def test_patient_can_book(
        self, patient_client, doctor_profile, availability, patient_profile, monday
    ):
        start = make_start(monday)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 201

    def test_doctor_cannot_book(
        self, doctor_client, doctor_profile, availability, monday
    ):
        start = make_start(monday)
        res = doctor_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 403

    def test_unauthenticated_cannot_book(
        self, anon_client, doctor_profile, availability, monday
    ):
        start = make_start(monday)
        res = anon_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 401

    def test_past_date_rejected(
        self, patient_client, doctor_profile, availability
    ):
        past = timezone.now() - timedelta(days=1)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": past.isoformat(),
            "end_time": (past + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 400

    def test_end_before_start_rejected(
        self, patient_client, doctor_profile, availability, monday
    ):
        start = make_start(monday)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start - timedelta(minutes=10)).isoformat(),
        })
        assert res.status_code == 400

    def test_outside_availability_hours_rejected(
        self, patient_client, doctor_profile, availability, monday
    ):
        # availability is 09:00–11:00; booking at 07:00
        start = make_start(monday, h=7)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 400

    def test_wrong_duration_rejected(
        self, patient_client, doctor_profile, availability, monday
    ):
        # slot_duration is 30 min; booking 60 min
        start = make_start(monday)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=60)).isoformat(),
        })
        assert res.status_code == 400

    def test_no_availability_on_day_rejected(
        self, patient_client, doctor_profile, monday
    ):
        # No availability created
        start = make_start(monday)
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 400

    def test_double_booking_rejected(
        self, patient_client, doctor_profile, availability, patient_profile, monday
    ):
        start = make_start(monday)
        # First booking
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.PENDING,
        )
        # Second booking same slot
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 400

    def test_cancelled_slot_can_be_rebooked(
        self, patient_client, doctor_profile, availability, patient_profile, monday
    ):
        start = make_start(monday)
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=start,
            end_time=start + timedelta(minutes=30),
            status=Appointment.Status.CANCELLED,
        )
        res = patient_client.post(APPT_URL, {
            "doctor": doctor_profile.pk,
            "start_time": start.isoformat(),
            "end_time": (start + timedelta(minutes=30)).isoformat(),
        })
        assert res.status_code == 201


@pytest.mark.django_db
class TestAppointmentListAndDetail:

    def test_patient_sees_own_appointments_only(
        self, patient_client, appointment, db
    ):
        res = patient_client.get(APPT_URL)
        assert res.status_code == 200
        for appt in res.data["results"]:
            assert appt["patient"] == appointment.patient.pk

    def test_doctor_sees_own_appointments_only(
        self, doctor_client, appointment
    ):
        res = doctor_client.get(APPT_URL)
        assert res.status_code == 200

    def test_admin_sees_all_appointments(self, admin_client, appointment):
        res = admin_client.get(APPT_URL)
        assert res.status_code == 200

    def test_filter_by_status(self, patient_client, appointment):
        res = patient_client.get(f"{APPT_URL}?status=PENDING")
        assert res.status_code == 200
        for appt in res.data["results"]:
            assert appt["status"] == "PENDING"

    def test_filter_upcoming(self, patient_client, appointment):
        res = patient_client.get(f"{APPT_URL}?type=upcoming")
        assert res.status_code == 200

    def test_filter_past(self, patient_client, appointment):
        res = patient_client.get(f"{APPT_URL}?type=past")
        assert res.status_code == 200


@pytest.mark.django_db
class TestCancelAppointment:

    def test_patient_can_cancel_pending(self, patient_client, appointment):
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"status": "CANCELLED"}
        )
        assert res.status_code == 200
        appointment.refresh_from_db()
        assert appointment.status == Appointment.Status.CANCELLED

    def test_patient_cannot_cancel_confirmed(
        self, patient_client, appointment
    ):
        appointment.status = Appointment.Status.CONFIRMED
        appointment.save()
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"status": "CANCELLED"}
        )
        assert res.status_code == 400

    def test_patient_cannot_set_confirmed(self, patient_client, appointment):
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"status": "CONFIRMED"}
        )
        assert res.status_code == 400

    def test_doctor_can_confirm(self, doctor_client, appointment):
        res = doctor_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"status": "CONFIRMED"}
        )
        assert res.status_code == 200
        appointment.refresh_from_db()
        assert appointment.status == Appointment.Status.CONFIRMED

    def test_doctor_can_add_notes(self, doctor_client, appointment):
        res = doctor_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"notes": "Bring previous reports."}
        )
        assert res.status_code == 200
        appointment.refresh_from_db()
        assert appointment.notes == "Bring previous reports."

    def test_doctor_cannot_set_back_to_pending(self, doctor_client, appointment):
        appointment.status = Appointment.Status.CONFIRMED
        appointment.save()
        res = doctor_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"status": "PENDING"}
        )
        assert res.status_code == 400

    def test_doctor_cannot_modify_completed_appointment(
        self, doctor_client, appointment
    ):
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        res = doctor_client.patch(
            f"{APPT_URL}{appointment.pk}/",
            {"notes": "Late note"}
        )
        assert res.status_code == 400

    def test_cannot_delete_appointment(self, patient_client, appointment):
        res = patient_client.delete(f"{APPT_URL}{appointment.pk}/")
        assert res.status_code == 405


@pytest.mark.django_db
class TestRescheduleAppointment:

    def test_patient_can_reschedule_pending(
        self, patient_client, appointment, availability, monday
    ):
        new_start = make_start(monday, h=9, m=30)
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/reschedule/",
            {"start_time": new_start.isoformat()}
        )
        assert res.status_code == 200
        appointment.refresh_from_db()
        assert appointment.start_time == new_start

    def test_cannot_reschedule_to_past(
        self, patient_client, appointment
    ):
        past = timezone.now() - timedelta(days=1)
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/reschedule/",
            {"start_time": past.isoformat()}
        )
        assert res.status_code == 400

    def test_cannot_reschedule_cancelled(
        self, patient_client, appointment, monday
    ):
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()
        new_start = make_start(monday, h=9, m=30)
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/reschedule/",
            {"start_time": new_start.isoformat()}
        )
        assert res.status_code == 400

    def test_cannot_reschedule_to_booked_slot(
        self, patient_client, appointment, patient_profile,
        doctor_profile, availability, monday
    ):
        occupied_start = make_start(monday, h=9, m=30)
        Appointment.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            availability=availability,
            start_time=occupied_start,
            end_time=occupied_start + timedelta(minutes=30),
            status=Appointment.Status.PENDING,
        )
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/reschedule/",
            {"start_time": occupied_start.isoformat()}
        )
        assert res.status_code == 400

    def test_cannot_reschedule_outside_availability(
        self, patient_client, appointment, monday
    ):
        # 07:00 is outside availability (09:00–11:00)
        outside = make_start(monday, h=7)
        res = patient_client.patch(
            f"{APPT_URL}{appointment.pk}/reschedule/",
            {"start_time": outside.isoformat()}
        )
        assert res.status_code == 400