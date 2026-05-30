from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from doctors.models import DoctorProfile, Specialty
from patients.models import PatientProfile
from appointments.models import Appointment
from availability.models import Availability


class PatientAppointmentListTests(APITestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='doctor1', email='doctor@test.com',
            password='testpass123', role='D',
            first_name='John', last_name='Doe'
        )
        self.specialty = Specialty.objects.create(name='General')
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user, specialty=self.specialty
        )
        self.patient_user = User.objects.create_user(
            username='patient1', email='patient@test.com',
            password='testpass123', role='P',
            first_name='Jane', last_name='Doe'
        )
        self.patient = PatientProfile.objects.create(user=self.patient_user)

        self.other_patient_user = User.objects.create_user(
            username='patient2', email='patient2@test.com',
            password='testpass123', role='P',
            first_name='Other', last_name='Patient'
        )
        self.other_patient = PatientProfile.objects.create(
            user=self.other_patient_user
        )

        self.start_time = timezone.now() + timedelta(days=7)
        self.end_time = self.start_time + timedelta(minutes=30)

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        # Another patient's appointment — should never appear in results
        self.other_appointment = Appointment.objects.create(
            patient=self.other_patient,
            doctor=self.doctor,
            start_time=self.start_time + timedelta(hours=1),
            end_time=self.start_time + timedelta(hours=1, minutes=30),
        )

        self.list_url = reverse('appointment-list')
        self.client.force_authenticate(user=self.patient_user)

    def test_patient_sees_only_own_appointments(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [a['id'] for a in response.data['results']]
        self.assertIn(self.appointment.id, ids)
        self.assertNotIn(self.other_appointment.id, ids)

    def test_unauthenticated_request_is_rejected(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_by_status(self):
        response = self.client.get(self.list_url, {'status': 'PENDING'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for appt in response.data['results']:
            self.assertEqual(appt['status'], 'PENDING')

    def test_filter_upcoming(self):
        response = self.client.get(self.list_url, {'type': 'upcoming'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [a['id'] for a in response.data['results']]
        self.assertIn(self.appointment.id, ids)

    def test_filter_past(self):
        response = self.client.get(self.list_url, {'type': 'past'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [a['id'] for a in response.data['results']]
        self.assertNotIn(self.appointment.id, ids)

    def test_patient_can_retrieve_own_appointment(self):
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)

    def test_patient_cannot_retrieve_other_patient_appointment(self):
        url = reverse('appointment-detail', args=[self.other_appointment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PatientAppointmentCancelTests(APITestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='doctor1', email='doctor@test.com',
            password='testpass123', role='D',
            first_name='John', last_name='Doe'
        )
        self.specialty = Specialty.objects.create(name='General')
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user, specialty=self.specialty
        )
        self.patient_user = User.objects.create_user(
            username='patient1', email='patient@test.com',
            password='testpass123', role='P',
            first_name='Jane', last_name='Doe'
        )
        self.patient = PatientProfile.objects.create(user=self.patient_user)

        self.start_time = timezone.now() + timedelta(days=7)
        self.end_time = self.start_time + timedelta(minutes=30)
        self.client.force_authenticate(user=self.patient_user)

    def _create_appointment(self, status=Appointment.Status.PENDING):
        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        if status != Appointment.Status.PENDING:
            appt.status = status
            appt.save()
        return appt

    def test_patient_can_cancel_pending_appointment(self):
        appt = self._create_appointment()
        url = reverse('appointment-detail', args=[appt.id])
        response = self.client.patch(url, {'status': 'CANCELLED'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.Status.CANCELLED)

    def test_patient_cannot_cancel_completed_appointment(self):
        appt = self._create_appointment(status=Appointment.Status.COMPLETED)
        url = reverse('appointment-detail', args=[appt.id])
        response = self.client.patch(url, {'status': 'CANCELLED'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_cannot_cancel_already_cancelled_appointment(self):
        appt = self._create_appointment(status=Appointment.Status.CANCELLED)
        url = reverse('appointment-detail', args=[appt.id])
        response = self.client.patch(url, {'status': 'CANCELLED'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_cannot_set_status_to_confirmed(self):
        appt = self._create_appointment()
        url = reverse('appointment-detail', args=[appt.id])
        response = self.client.patch(url, {'status': 'CONFIRMED'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PatientAppointmentRescheduleTests(APITestCase):

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='doctor1', email='doctor@test.com',
            password='testpass123', role='D',
            first_name='John', last_name='Doe'
        )
        self.specialty = Specialty.objects.create(name='General')
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user, specialty=self.specialty
        )
        self.patient_user = User.objects.create_user(
            username='patient1', email='patient@test.com',
            password='testpass123', role='P',
            first_name='Jane', last_name='Doe'
        )
        self.patient = PatientProfile.objects.create(user=self.patient_user)

        # Future Monday
        self.monday = timezone.now() + timedelta(days=(7 - timezone.now().weekday()))
        self.monday = self.monday.replace(hour=9, minute=0, second=0, microsecond=0)

        Availability.objects.create(
            doctor=self.doctor,
            day_of_week=self.monday.weekday(),
            start_time=self.monday.time(),
            end_time=(self.monday + timedelta(hours=4)).time(),
            slot_duration_minutes=60,
            is_active=True
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time=self.monday,
            end_time=self.monday + timedelta(hours=1),
        )

        self.reschedule_url = reverse(
            'appointment-reschedule', args=[self.appointment.id]
        )
        self.client.force_authenticate(user=self.patient_user)

    def test_patient_can_reschedule_to_available_slot(self):
        new_start = self.monday + timedelta(hours=2)
        response = self.client.patch(
            self.reschedule_url,
            {'start_time': new_start.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(
            self.appointment.start_time,
            new_start
        )
        self.assertEqual(
            self.appointment.end_time,
            new_start + timedelta(hours=1)
        )

    def test_cannot_reschedule_to_past_time(self):
        past_time = timezone.now() - timedelta(hours=1)
        response = self.client.patch(
            self.reschedule_url,
            {'start_time': past_time.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_reschedule_outside_availability(self):
        # 3AM is outside 9AM-1PM availability
        out_of_hours = self.monday.replace(hour=3)
        response = self.client.patch(
            self.reschedule_url,
            {'start_time': out_of_hours.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_reschedule_to_already_booked_slot(self):
        other_patient_user = User.objects.create_user(
            username='patient2', email='patient2@test.com',
            password='testpass123', role='P',
            first_name='Other', last_name='Patient'
        )
        other_patient = PatientProfile.objects.create(user=other_patient_user)
        booked_start = self.monday + timedelta(hours=2)
        Appointment.objects.create(
            patient=other_patient,
            doctor=self.doctor,
            start_time=booked_start,
            end_time=booked_start + timedelta(hours=1),
        )

        response = self.client.patch(
            self.reschedule_url,
            {'start_time': booked_start.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_reschedule_cancelled_appointment(self):
        self.appointment.status = Appointment.Status.CANCELLED
        self.appointment.save()

        new_start = self.monday + timedelta(hours=2)
        response = self.client.patch(
            self.reschedule_url,
            {'start_time': new_start.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_reschedule_completed_appointment(self):
        self.appointment.status = Appointment.Status.COMPLETED
        self.appointment.save()

        new_start = self.monday + timedelta(hours=2)
        response = self.client.patch(
            self.reschedule_url,
            {'start_time': new_start.isoformat()},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)