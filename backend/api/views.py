from django.contrib.auth import get_user_model
from django.db.migrations import serializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from .models import Product
from .serializers import ProductSerializer
from users.serializers import EmptySerializer

from rest_framework.views import APIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

import logging

logger = logging.getLogger(__name__)
# User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({"message": "CSRF cookie set"})


class RandomProductView(APIView):
    @extend_schema(
        summary="Get a random product",
        description="Returns a random product from the database. If no products are available, returns a 404 error.",
    )
    def get(self, request):
        product = Product.objects.order_by("?").first()
        if product:
            return Response(ProductSerializer(product).data)
        return Response({"error": "No products available"}, status=404)


class ProductItemsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(
        detail=True, methods=["get"], authentication_classes=[], permission_classes=[]
    )
    def is_registered(self, request, pk):  # Placeholder action
        return Response({"message": f"registered {pk}"})


class ProductViewSet(ModelViewSet):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"] # Default


# class ProductDetailView(RetrieveAPIView):
#     permission_classes = []
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductReadOnlyViewSet(ReadOnlyModelViewSet):
#     permission_classes = []
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
