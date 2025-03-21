from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product", price=10.00, description="Test Description"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 10.00)
        self.assertEqual(self.product.description, "Test Description")


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product", price=10.00, description="Test Description"
        )
        self.serializer = ProductSerializer(instance=self.product)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["id", "name", "price", "description"]))
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["price"], "10.00")
        self.assertEqual(data["description"], "Test Description")


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product", price=10.00, description="Test Description"
        )

    def test_get_random_product(self):
        response = self.client.get("/api/random/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn("price", response.data)
        self.assertIn("description", response.data)

    def test_product_list(self):
        response = self.client.get("/api/products1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Product")