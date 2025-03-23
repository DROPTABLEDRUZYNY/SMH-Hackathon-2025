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
        self.logout_url = reverse("users-logout")

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

    def test_logout_authenticated_user(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)
        data = {"refresh": str(refresh)}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.client.force_authenticate(user=None)

    def test_logout_invalid_token(self):
        self.client.force_authenticate(user=self.user)
        data = {"refresh": "invalidtoken"}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.force_authenticate(user=None)

    def test_get_user_current(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_get_user_current_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "test@example.com")


class JWTAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        self.client = APIClient()

    def test_obtain_token(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        if "refresh" in response.data:
            self.assertTrue(response.data["refresh"])
        if "access" in response.data:
            self.assertTrue(response.data["access"])

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        url = reverse("token_verify")
        response = self.client.post(url, {"token": str(access)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_view_with_valid_token(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_access_protected_view_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalidtoken")
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_view_without_token(self):
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_request_user_is_authenticated(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access))
        url = reverse("user_current")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
