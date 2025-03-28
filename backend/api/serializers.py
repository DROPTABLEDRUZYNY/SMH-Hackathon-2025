from rest_framework import serializers
from .models import Product, Event

import logging

logger = logging.getLogger(__name__)


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


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "date_start",
            "latitude",
            "longitude",
            # "participants",
        ]
        
    def create(self, validated_data):
        logger.info(f"Creating new event with data: {validated_data}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info(f"Updating event {instance.id} with data: {validated_data}")
        return super().update(instance, validated_data)

