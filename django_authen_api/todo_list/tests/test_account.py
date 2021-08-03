from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class AccountTests(APITestCase):

    def setUp(self):
        user = User.objects.create(username= "trung", password=make_password("12345678"))

    def test_create_account_success(self):
        """
            Ensure create new account successfully !
        """
        url = reverse("account_register")
        body = {
            "username" : "trung_1",
            "password" : "123456789"
        }

        response = self.client.post(url, data=body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_not_allow_create_dupplicate_account(self):
        """
            Ensure duplicate account should not be registered !
        """
        url = reverse("account_register")

        body = {
            "username" : "trung",
            "password" : "12345678"
        }

        response = self.client.post(url, data=body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_successfully_with_valid_account(self):
        """
            Ensure valid account login successfully !
        """

        url = reverse("account_login")

        body = {
            "username" : "trung",
            "password" : "12345678"
        }
        response = self.client.post(url, data=body, format='json')
        self.assertEqual(response.status_code, status.HTTP_307_TEMPORARY_REDIRECT)





