import pytest
from datetime import date, timedelta


PATIENT_ME_URL = "/patients/patient/me/"


@pytest.mark.django_db
class TestPatientProfile:

    def test_patient_can_get_own_profile(self, patient_client, patient_profile):
        res = patient_client.get(PATIENT_ME_URL)
        assert res.status_code == 200
        assert res.data["data"]["email"] == patient_profile.user.email

    def test_patient_can_update_profile(self, patient_client, patient_profile):
        res = patient_client.patch(PATIENT_ME_URL, {
            "phone": "01234567890",
            "gender": "M",
            "address": "123 Main St",
        })
        assert res.status_code == 200
        assert res.data["data"]["phone"] == "01234567890"

    def test_doctor_cannot_access_patient_profile(self, doctor_client):
        res = doctor_client.get(PATIENT_ME_URL)
        assert res.status_code == 403

    def test_unauthenticated_blocked(self, anon_client):
        res = anon_client.get(PATIENT_ME_URL)
        assert res.status_code == 401

    def test_future_date_of_birth_rejected(self, patient_client, patient_profile):
        future = (date.today() + timedelta(days=1)).isoformat()
        res = patient_client.patch(PATIENT_ME_URL, {"date_of_birth": future})
        assert res.status_code == 400

    def test_valid_date_of_birth_accepted(self, patient_client, patient_profile):
        res = patient_client.patch(PATIENT_ME_URL, {"date_of_birth": "1995-06-15"})
        assert res.status_code == 200
        assert res.data["data"]["date_of_birth"] == "1995-06-15"

    def test_invalid_gender_rejected(self, patient_client, patient_profile):
        res = patient_client.patch(PATIENT_ME_URL, {"gender": "X"})
        assert res.status_code == 400

    def test_profile_auto_created_if_missing(self, patient_client, patient_user):
        # patient_profile fixture not used — profile should be created on demand
        res = patient_client.get(PATIENT_ME_URL)
        assert res.status_code == 200