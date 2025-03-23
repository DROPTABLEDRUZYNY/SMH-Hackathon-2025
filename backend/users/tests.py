from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from django.urls import reverse

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="firstNAME",
            last_name="lastNAME",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(
            self.user.first_name, "Firstname"
        )  # Test capitalizing first name
        self.assertEqual(self.user.last_name, "Lastname")  # Test capitalizing last name


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "first_name", "last_name", "email", "birth_date"]),
        )
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        self.register_url = reverse("users-register")
        self.login_url = reverse("rest_framework:login")
        self.logout_url = reverse("rest_framework:logout")
        self.current_user_url = reverse("user_current")

    def test_register_new_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "birth_date": "2000-01-01",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "newuser@example.com")

    def test_register_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "birth_date": "2000-01-01",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=None)

    def test_register_invalid_data(self):
        data = {
            "email": "invalidemail",
            "password": "short",
            "first_name": "",
            "last_name": "",
            "birth_date": "invalid-date",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        data = {
            "username": self.user.email,
            "password": "password123",
        }
        login_url_with_next = f"{self.login_url}?next=/api/"
        response = self.client.post(login_url_with_next, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_get_current_user_unauthenticated(self):
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
