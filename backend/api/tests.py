from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import datetime, make_aware
from rest_framework.authentication import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Activity, Product, TrashPlace
from .serializers import ProductSerializer, TrashPlaceSerializer

User = get_user_model()


class EventModelTest(TestCase):
    def setUp(self):
        self.event = TrashPlace.objects.create(
            name="Test Event",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
        )

    def test_event_creation(self):
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.description, "Test Description")
        self.assertEqual(self.event.latitude, 52.2297)
        self.assertEqual(self.event.longitude, 21.0122)


class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.trash_place = TrashPlace.objects.create(
            name="Test Trash Place",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
        )
        self.activity = Activity.objects.create(
            description="Test Activity",
            trash_place=self.trash_place,
            user=self.user,
            collected_kg=10.5,
            cleaned_all=True,
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.description, "Test Activity")
        self.assertEqual(self.activity.trash_place, self.trash_place)
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.collected_kg, 10.5)
        self.assertTrue(self.activity.cleaned_all)


class TrashPlaceModelTest(TestCase):
    def setUp(self):
        self.trash_place = TrashPlace.objects.create(
            name="Test Trash Place",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
            is_active=True,
        )

    def test_trash_place_creation(self):
        self.assertEqual(self.trash_place.name, "Test Trash Place")
        self.assertEqual(self.trash_place.description, "Test Description")
        self.assertEqual(self.trash_place.latitude, 52.2297)
        self.assertEqual(self.trash_place.longitude, 21.0122)
        self.assertTrue(self.trash_place.is_active)

    def test_trash_place_string_representation(self):
        self.assertEqual(
            str(self.trash_place),
            f"{self.trash_place.name} ({self.trash_place.pk}) {self.trash_place.date_created}",
        )


class ActivityViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.trash_place = TrashPlace.objects.create(
            name="Test Trash Place",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        url = reverse("activities-list")  # Poprawiona nazwa
        data = {
            "description": "Test Activity",
            "trash_place_id": self.trash_place.id,
            "collected_kg": 10.5,
            "cleaned_all": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        activity = Activity.objects.first()
        self.assertEqual(activity.description, "Test Activity")
        self.assertEqual(activity.trash_place, self.trash_place)
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.collected_kg, 10.5)
        self.assertTrue(activity.cleaned_all)

    def test_list_activities(self):
        Activity.objects.create(
            description="Test Activity",
            trash_place=self.trash_place,
            user=self.user,
            collected_kg=10.5,
            cleaned_all=True,
        )
        url = reverse("activities-list")  # Poprawiona nazwa
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Test Activity")


class TrashPlaceViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.trash_place = TrashPlace.objects.create(
            name="Test Trash Place",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
            is_active=True,
        )

    def test_list_trash_places(self):
        url = reverse("trash_places-list") 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Trash Place")

    def test_retrieve_trash_place(self):
        url = reverse("trash_places-detail", args=[self.trash_place.id])  # Poprawiona nazwa
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Trash Place")
        self.assertEqual(response.data["description"], "Test Description")
        self.assertEqual(response.data["latitude"], 52.2297)
        self.assertEqual(response.data["longitude"], 21.0122)
        self.assertTrue(response.data["is_active"])
