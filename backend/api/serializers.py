from rest_framework import serializers
from .models import Product, TrashPlace, Activity

import logging

logger = logging.getLogger(__name__)


class TrashPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrashPlace
        fields = [
            "id",
            "name",
            "description",
            "date_created",
            "latitude",
            "longitude",
            "is_active",
        ]


class ActivitySerializer(serializers.ModelSerializer):
    trash_place = TrashPlaceSerializer(
        read_only=True
    ) 
    trash_place_id = serializers.PrimaryKeyRelatedField(
        queryset=TrashPlace.objects.all(), source="trash_place", write_only=True
    )

    class Meta:
        model = Activity
        fields = [
            "id",
            "description",
            "date",
            "trash_place_id",
            "trash_place",
            "collected_kg",
            "cleaned_all",
            "before_image",
            "after_image",
        ]

class ProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        logger.info(f"Creating new product with data: {validated_data}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info(f"Updating product {instance.id} with data: {validated_data}")
        return super().update(instance, validated_data)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description"]
