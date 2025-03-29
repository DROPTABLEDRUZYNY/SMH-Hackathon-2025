from django.contrib.auth import get_user_model
from django.db.migrations import serializer
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from .models import Product, TrashPlace, Activity
from .serializers import ProductSerializer, TrashPlaceSerializer, ActivitySerializer
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
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({"message": "CSRF cookie set"})


class TrashPlaceListViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = []
    queryset = TrashPlace.objects.all()
    serializer_class = TrashPlaceSerializer


class ActivityViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = (
            User.objects.annotate(
                total_kg=Coalesce(Sum("activities__collected_kg"), Value(0.0)),
                total_activities=Coalesce(Count("activities"), Value(0)),
            )
            .order_by("-total_kg")
            .values("id", "first_name", "last_name", "total_kg", "total_activities")[
                :10
            ]
        )

        formatted_users = [
            {
                "id": user["id"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "total_kg": float(user["total_kg"]),
                "total_activities": user["total_activities"],
            }
            for user in users
        ]

        return Response(formatted_users)


# ==================================================
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
