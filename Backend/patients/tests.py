from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from Backend.patients.models import PatientProfile

User = get_user_model()


class PatientProfileRetrieveTests(APITestCase):

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            role='P',
            is_approved=True,
            is_blocked=False
        )
        self.profile = PatientProfile.objects.create(
            user=self.patient,
            phone='01012345678',
            gender='M',
        )
        self.url = reverse('patient-profile-me')

    def test_patient_can_retrieve_own_profile(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['phone'], '01012345678')

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_cannot_access_patient_profile(self):
        doctor = User.objects.create_user(
            username='doctor1',
            email='doctor@test.com',
            password='testpass123',
            role='D',
            is_approved=True,
            is_blocked=False
        )
        self.client.force_authenticate(user=doctor)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PatientProfileUpdateTests(APITestCase):

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            role='P',
            is_approved=True,
            is_blocked=False
        )
        self.profile = PatientProfile.objects.create(
            user=self.patient,
            phone='01012345678',
            gender='M',
        )
        self.url = reverse('patient-profile-me')
        self.client.force_authenticate(user=self.patient)

    def test_patient_can_update_own_profile(self):
        response = self.client.patch(self.url, {'phone': '01099999999', 'gender': 'F'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['phone'], '01099999999')
        self.assertEqual(response.data['data']['gender'], 'F')

    def test_partial_update_does_not_wipe_other_fields(self):
        response = self.client.patch(self.url, {'phone': '01011111111'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['gender'], 'M')  # unchanged


class PatientProfileValidationTests(APITestCase):

    def setUp(self):
        self.patient = User.objects.create_user(
            username='patient1',
            email='patient@test.com',
            password='testpass123',
            role='P',
            is_approved=True,
            is_blocked=False
        )
        PatientProfile.objects.create(user=self.patient, phone='01012345678')
        self.url = reverse('patient-profile-me')
        self.client.force_authenticate(user=self.patient)

    def test_future_date_of_birth_is_rejected(self):
        response = self.client.patch(self.url, {'date_of_birth': '2099-01-01'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')