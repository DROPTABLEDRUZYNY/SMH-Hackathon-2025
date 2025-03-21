from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")


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
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        response = self.client.get("/users/current/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_user_list(self):
        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "test@example.com")

    def test_get_current_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/users/current/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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
        response = self.client.post(
            "/users/token/", {"email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post("/users/token/refresh/", {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        response = self.client.post("/users/token/verify/", {"token": str(access)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_view_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalidtoken")
        response = self.client.get("/users/current/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_protected_view_without_token(self):
        response = self.client.get("/users/current/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
