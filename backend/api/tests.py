from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import datetime, make_aware
from rest_framework.authentication import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Product, TrashPlace
from .serializers import ProductSerializer, EventSerializer, TrashPlaceSerializer

User = get_user_model()

# class ProductModelTest(TestCase):
#     def setUp(self):
#         self.product = Product.objects.create(
#             name="Test Product", price=10.00, description="Test Description"
#         )

#     def test_product_creation(self):
#         self.assertEqual(self.product.name, "Test Product")
#         self.assertEqual(self.product.price, 10.00)
#         self.assertEqual(self.product.description, "Test Description")


# class ProductSerializerTest(TestCase):
#     def setUp(self):
#         self.product = Product.objects.create(
#             name="Test Product", price=10.00, description="Test Description"
#         )
#         self.serializer = ProductSerializer(instance=self.product)

#     def test_serializer_fields(self):
#         data = self.serializer.data
#         self.assertEqual(set(data.keys()), set(["id", "name", "price", "description"]))
#         self.assertEqual(data["name"], "Test Product")
#         self.assertEqual(data["price"], "10.00")
#         self.assertEqual(data["description"], "Test Description")


# class ProductAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.product = Product.objects.create(
#             name="Test Product", price=10.00, description="Test Description"
#         )

#     def test_get_random_product(self):
#         url = reverse("random_product")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("name", response.data)
#         self.assertIn("price", response.data)
#         self.assertIn("description", response.data)

#     def test_product_list(self):
#         url = reverse("products1-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["name"], "Test Product")


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


class EventSerializerTest(TestCase):
    def setUp(self):
        self.event = TrashPlace.objects.create(
            name="Test Event",
            description="Test Description",
            latitude=52.2297,
            longitude=21.0122,
        )
        self.serializer = TrashPlaceSerializer(instance=self.event)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(["id", "name", "description", "date_created", "latitude", "longitude", "is_active"]),
        )
        self.assertEqual(data["name"], "Test Event")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["latitude"], 52.2297)
        self.assertEqual(data["longitude"], 21.0122)


class EventAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = TrashPlace.objects.create(
            name="Test Event",
            description="Test Description",
            date_start="2025-03-28T10:00:00Z",
            latitude=52.2297,
            longitude=21.0122,
        )
        self.event_list_url = reverse("event-list")


