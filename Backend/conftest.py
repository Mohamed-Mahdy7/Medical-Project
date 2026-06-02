import pytest
from django.utils import timezone
from datetime import timedelta, time
from rest_framework.test import APIClient
from accounts.models import User
from doctors.models import DoctorProfile, Specialty
from patients.models import PatientProfile
from availability.models import Availability
from appointments.models import Appointment


# ── helpers ──────────────────────────────────────────────────────────────────

def make_user(username, role, password="Pass1234!", **kwargs):
    return User.objects.create_user(
        username=username,
        email=f"{username}@test.com",
        first_name="Test",
        last_name="User",
        password=password,
        role=role,
        is_approved=True,
        is_blocked=False,
        **kwargs,
    )


def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# ── fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def patient_user(db):
    return make_user("patient1", User.Roles.PATIENT)


@pytest.fixture
def doctor_user(db):
    return make_user("doctor1", User.Roles.DOCTOR)


@pytest.fixture
def admin_user(db):
    return make_user("admin1", User.Roles.PATIENT, is_staff=True, is_superuser=True)


@pytest.fixture
def specialty(db):
    return Specialty.objects.create(name="Cardiology", description="Heart specialist")


@pytest.fixture
def doctor_profile(db, doctor_user, specialty):
    return DoctorProfile.objects.create(
        user=doctor_user,
        specialty=specialty,
        phone="01000000000",
        bio="Test bio",
        years_of_experience=5,
    )


@pytest.fixture
def patient_profile(db, patient_user):
    return PatientProfile.objects.create(user=patient_user)


@pytest.fixture
def availability(db, doctor_profile):
    # Monday 09:00–11:00, 30-min slots
    return Availability.objects.create(
        doctor=doctor_profile,
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(11, 0),
        slot_duration_minutes=30,
        price=200,
        is_active=True,
    )


def next_weekday(weekday):
    """Return the next date that falls on `weekday` (0=Mon) from today."""
    today = timezone.now().date()
    days_ahead = (weekday - today.weekday()) % 7 or 7
    return today + timedelta(days=days_ahead)


@pytest.fixture
def monday():
    return next_weekday(0)


@pytest.fixture
def appointment(db, patient_profile, doctor_profile, availability, monday):
    start = timezone.make_aware(
        timezone.datetime.combine(monday, time(9, 0))
    )
    end = start + timedelta(minutes=30)
    return Appointment.objects.create(
        patient=patient_profile,
        doctor=doctor_profile,
        availability=availability,
        start_time=start,
        end_time=end,
        status=Appointment.Status.PENDING,
    )


@pytest.fixture
def patient_client(patient_user):
    return auth_client(patient_user)


@pytest.fixture
def doctor_client(doctor_user):
    return auth_client(doctor_user)


@pytest.fixture
def admin_client(admin_user):
    return auth_client(admin_user)


@pytest.fixture
def anon_client():
    return APIClient()