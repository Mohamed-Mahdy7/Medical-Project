import pytest
from django.urls import reverse
from accounts.models import User


REGISTER_URL = "/accounts/user/"
LOGIN_URL    = "/accounts/login/"
ME_URL       = "/accounts/user/me/"


@pytest.mark.django_db
class TestUserRegistration:

    def test_patient_registers_successfully(self, anon_client):
        res = anon_client.post(REGISTER_URL, {
            "username": "newpatient",
            "email": "newpatient@test.com",
            "first_name": "New",
            "last_name": "Patient",
            "password": "StrongPass1!",
            "confirm_password": "StrongPass1!",
            "role": "P",
        })
        assert res.status_code == 200
        assert User.objects.filter(username="newpatient").exists()

    def test_doctor_registers_successfully(self, anon_client):
        res = anon_client.post(REGISTER_URL, {
            "username": "newdoctor",
            "email": "newdoctor@test.com",
            "first_name": "New",
            "last_name": "Doctor",
            "password": "StrongPass1!",
            "confirm_password": "StrongPass1!",
            "role": "D",
        })
        assert res.status_code == 200
        assert User.objects.filter(username="newdoctor").exists()

    def test_mismatched_passwords_rejected(self, anon_client):
        res = anon_client.post(REGISTER_URL, {
            "username": "baduser",
            "email": "bad@test.com",
            "first_name": "Bad",
            "last_name": "User",
            "password": "StrongPass1!",
            "confirm_password": "WrongPass1!",
            "role": "P",
        })
        assert res.status_code == 400

    def test_duplicate_username_rejected(self, anon_client, patient_user):
        res = anon_client.post(REGISTER_URL, {
            "username": patient_user.username,
            "email": "other@test.com",
            "first_name": "Dup",
            "last_name": "User",
            "password": "StrongPass1!",
            "confirm_password": "StrongPass1!",
            "role": "P",
        })
        assert res.status_code == 400

    def test_duplicate_email_rejected(self, anon_client, patient_user):
        res = anon_client.post(REGISTER_URL, {
            "username": "uniqueuser",
            "email": patient_user.email,
            "first_name": "Dup",
            "last_name": "Email",
            "password": "StrongPass1!",
            "confirm_password": "StrongPass1!",
            "role": "P",
        })
        assert res.status_code == 400

    def test_missing_role_rejected(self, anon_client):
        res = anon_client.post(REGISTER_URL, {
            "username": "norole",
            "email": "norole@test.com",
            "first_name": "No",
            "last_name": "Role",
            "password": "StrongPass1!",
            "confirm_password": "StrongPass1!",
        })
        assert res.status_code == 400


@pytest.mark.django_db
class TestLogin:

    def test_valid_credentials_return_cookies(self, anon_client, patient_user):
        res = anon_client.post(LOGIN_URL, {
            "username": patient_user.username,
            "password": "Pass1234!",
        })
        assert res.status_code == 200
        assert "access_token" in res.cookies
        assert "refresh_token" in res.cookies
        assert res.data == {"message": "Login Successfully!"}

    def test_wrong_password_rejected(self, anon_client, patient_user):
        res = anon_client.post(LOGIN_URL, {
            "username": patient_user.username,
            "password": "WrongPassword",
        })
        assert res.status_code == 401

    def test_nonexistent_user_rejected(self, anon_client):
        res = anon_client.post(LOGIN_URL, {
            "username": "ghost",
            "password": "Pass1234!",
        })
        assert res.status_code == 401


@pytest.mark.django_db
class TestMeEndpoint:

    def test_authenticated_user_gets_own_data(self, patient_client, patient_user):
        res = patient_client.get(ME_URL)
        assert res.status_code == 200
        assert res.data["username"] == patient_user.username
        assert res.data["role"] == "P"

    def test_unauthenticated_user_blocked(self, anon_client):
        res = anon_client.get(ME_URL)
        assert res.status_code == 401


@pytest.mark.django_db
class TestUserListPermissions:

    def test_admin_can_list_all_users(self, admin_client):
        res = admin_client.get(REGISTER_URL)
        assert res.status_code == 200

    def test_patient_cannot_list_all_users(self, patient_client):
        res = patient_client.get(REGISTER_URL)
        assert res.status_code == 403

    def test_filter_by_role_returns_only_doctors(self, admin_client, doctor_user, patient_user):
        res = admin_client.get(REGISTER_URL + "?role=D")
        assert res.status_code == 200
        usernames = [u["username"] for u in res.data["results"]]
        assert doctor_user.username in usernames
        assert patient_user.username not in usernames