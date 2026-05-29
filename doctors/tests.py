from datetime import date, time, datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from doctors.models import DoctorProfile, Specialty
from availability.models import Availability
from appointments.models import Appointment
from patients.models import PatientProfile
from doctors.utils import generate_available_slots

User = get_user_model()


class GenerateAvailableSlotsTests(APITestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='doctor1',
            email='doctor@test.com',
            password='testpass123',
            role='D',
            is_approved=True,
            is_blocked=False
        )
        self.specialty = Specialty.objects.create(name='General')
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty=self.specialty,
        )
        self.patient_user = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            role='P',
            is_approved=True,
            is_blocked=False
        )
        self.patient = PatientProfile.objects.create(user=self.patient_user)

        # 2026-06-01 is a Monday
        self.monday = date(2026, 6, 1)

    def _create_availability(self, start, end, duration=60):
        return Availability.objects.create(
            doctor=self.doctor,
            day_of_week=0,  # Monday
            start_time=start,
            end_time=end,
            slot_duration_minutes=duration,
            is_active=True
        )

    def _book_slot(self, slot_time, duration_minutes=60, status=Appointment.Status.CONFIRMED):
        start_dt = datetime.combine(self.monday, slot_time)
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        # Use timezone-aware datetimes to satisfy Appointment.clean()
        from django.utils import timezone
        import zoneinfo
        tz = zoneinfo.ZoneInfo('UTC')
        start_dt = timezone.make_aware(start_dt, tz) if timezone.is_naive(start_dt) else start_dt
        end_dt = timezone.make_aware(end_dt, tz) if timezone.is_naive(end_dt) else end_dt

        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            start_time=start_dt,
            end_time=end_dt,
            status=status
        )

    # --- Test 1 ---
    def test_no_availability_returns_empty(self):
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, [])

    # --- Test 2 ---
    def test_full_availability_no_bookings_returns_all_slots(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, ['09:00', '10:00'])

    # --- Test 3 ---
    def test_booked_slot_is_excluded(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        self._book_slot(time(9, 0))
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertNotIn('09:00', slots)
        self.assertIn('10:00', slots)

    # --- Test 4 ---
    def test_fully_booked_returns_empty(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        self._book_slot(time(9, 0))
        self._book_slot(time(10, 0))
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, [])

    # --- Test 5 ---
    def test_inactive_availability_is_ignored(self):
        Availability.objects.create(
            doctor=self.doctor,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(11, 0),
            slot_duration_minutes=60,
            is_active=False
        )
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, [])

    # --- Test 6 ---
    def test_pending_appointment_is_also_excluded(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        self._book_slot(time(9, 0), status=Appointment.Status.PENDING)
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertNotIn('09:00', slots)

    # --- Test 7 ---
    def test_cancelled_appointment_does_not_block_slot(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        self._book_slot(time(9, 0), status=Appointment.Status.CANCELLED)
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertIn('09:00', slots)

    # --- Test 8 ---
    def test_multiple_availability_windows_same_day(self):
        self._create_availability(time(9, 0), time(10, 0), duration=60)
        self._create_availability(time(14, 0), time(15, 0), duration=60)
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, ['09:00', '14:00'])

    # --- Test 9 ---
    def test_slot_duration_not_fitting_is_excluded(self):
        # 9:00-10:00 with 45min slots → only 09:00 fits, 09:45+45min goes past 10:00
        self._create_availability(time(9, 0), time(10, 0), duration=45)
        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertEqual(slots, ['09:00'])

    # --- Test 10 ---
    def test_wrong_day_returns_empty(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)
        tuesday = date(2026, 6, 2)  # Tuesday
        slots = generate_available_slots(self.doctor.id, tuesday)
        self.assertEqual(slots, [])

    # --- Test 11 ---
    def test_other_doctor_bookings_do_not_affect_slots(self):
        self._create_availability(time(9, 0), time(11, 0), duration=60)

        # Create a second doctor and book the same slot
        other_user = User.objects.create_user(
            username='doctor2',
            email='doctor2@test.com',
            password='testpass123',
            role='D',
            is_approved=True,
            is_blocked=False
        )
        other_doctor = DoctorProfile.objects.create(
            user=other_user,
            specialty=self.specialty,
        )
        start_dt = datetime.combine(self.monday, time(9, 0))
        end_dt = start_dt + timedelta(hours=1)
        from django.utils import timezone
        import zoneinfo
        tz = zoneinfo.ZoneInfo('UTC')
        Appointment.objects.create(
            doctor=other_doctor,
            patient=self.patient,
            start_time=timezone.make_aware(start_dt, tz),
            end_time=timezone.make_aware(end_dt, tz),
            status=Appointment.Status.CONFIRMED
        )

        slots = generate_available_slots(self.doctor.id, self.monday)
        self.assertIn('09:00', slots)