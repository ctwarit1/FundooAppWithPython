import pytest
from rest_framework.reverse import reverse


class TestUser:

    @pytest.mark.django_db
    def test_reg_successful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "kajri",
            "email": "ctwarit1@gmail.com",
            "password": "00000",
            "location": "kota",
            "phone": "7777777"
        }
        url = reverse('UserReg')
        response = client.post(url, user_data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_reg_unsuccessful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "",
            "email": "ctwarit1@gmail.com",
            "password": "00000",
            "location": "kota",
            "phone": "7777777"
        }
        url = reverse('UserReg')
        response = client.post(url, user_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_login_successful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "kajri",
            "email": "ctwarit1@gmail.com",
            "password": "00000",
            "location": "kota",
            "phone": "7777777",
            "is_verified": True,
        }
        url = reverse('UserReg')
        response = client.post(url, user_data)
        login_data = {
            "username": "kajri",
            "password": "00000"
        }
        url = reverse('UserLogin')
        response = client.post(url, login_data)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_login_unsuccessful(self, client, django_user_model):
        user_data = {
            "first_name": "twarit",
            "last_name": "chokniwal",
            "username": "kajri",
            "email": "ctwarit1@gmail.com",
            "password": "00000",
            "location": "kota",
            "phone": "7777777",
            "is_verified": True,
        }
        url = reverse('UserReg')
        response = client.post(url, user_data)
        login_data = {
            "username": "kajri",
            "password": ""
        }
        url = reverse('UserLogin')
        response = client.post(url, login_data)
        assert response.status_code == 400

