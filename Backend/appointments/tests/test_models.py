from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from Backend.accounts.models import User
from Backend.doctors.models import DoctorProfile, Specialty
from Backend.patients.models import PatientProfile
from Backend.appointments.models import Appointment

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username="doctor1",
            email="doctor1@email.com",
            password="testing321",
            first_name="first",
            last_name="doctor",
            role="D"
        )
        self.specialty = Specialty.objects.create(name="Cardiology")
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialty=self.specialty,
            phone="01234567890",
        )

        self.patient_user = User.objects.create_user(
            username="patient1",
            email="patient1@email.com",
            password="testing321",
            first_name="first",
            last_name="patient",
            role="P"
        )

        self.patient = PatientProfile.objects.create(
            user=self.patient_user,
            phone="01098765432",
        )
        
        self.start_time = timezone.now() + timedelta(days=7)
        self.end_time = self.start_time + timedelta(minutes=30)


    def test_valid_appointment_creates_successfully(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        self.assertIsNotNone(appointment.pk)
        self.assertEqual(appointment.status, Appointment.Status.PENDING)

    def test_end_time_before_start_time(self):
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                start_time=self.start_time,
                end_time=self.start_time - timedelta(minutes=30),
            )

    def test_end_time_equal_to_start_time(self):
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                start_time=self.start_time,
                end_time=self.start_time,
            )

    def test_booking_in_the_past(self):
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                start_time=timezone.now() - timedelta(days=1),
                end_time=timezone.now() - timedelta(hours=23)
            )

    def test_overlapping_appointment_raises_error(self):
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )

        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient,
                doctor=self.doctor,
                start_time=self.start_time + timedelta(minutes=15),
                end_time=self.end_time + timedelta(minutes=15),
            )

    def test_cancelled_slot_can_be_rebooked(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        appointment.status = Appointment.Status.CANCELLED
        appointment.save()

        new_appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time
        )
        self.assertIsNotNone(new_appointment.pk)

    def test_status_update_does_not_trigger_past_check(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time
        )

        appointment.start_time = timezone.now() - timedelta(hours=2)
        appointment.end_time = timezone.now() - timedelta(hours=1)
        appointment.status = Appointment.Status.COMPLETED
        appointment.save()
        self.assertEqual(appointment.status, Appointment.Status.COMPLETED)

    def test_default_status_is_pending(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        self.assertEqual(appointment.status, Appointment.Status.PENDING)

    def test_str_representation(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        expected = f"{self.patient} -> {self.doctor} | {self.start_time}"
        self.assertEqual(str(appointment), expected)