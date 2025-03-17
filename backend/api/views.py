from django.contrib.auth import get_user_model
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import action, api_view

from django.http import JsonResponse

from .models import Product
from .serializers import ProductSerializer

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

User = get_user_model()


@api_view(["GET"])
def api_home(request):
    serializer = ProductSerializer(Product.objects.order_by("?").first(), many=False)
    return Response(serializer.data)


class ProductDetailView(RetrieveAPIView):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request):
    #     student_groups = StudentGroup.objects.all()
    #     serializer = StudentGroupSerializer(student_groups, many=True)
    #     return Response(serializer.data)


class ProductItemsView(ListModelMixin,RetrieveModelMixin, GenericViewSet):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], authentication_classes=[], permission_classes=[])
    def is_registered(self, request,pk):  # Placeholder action
        return Response({'message': f'registered {pk}'})
    
class ProductViewSet(ModelViewSet):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductReadOnlyViewSet(ReadOnlyModelViewSet):
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer