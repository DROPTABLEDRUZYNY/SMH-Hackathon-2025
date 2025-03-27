from rest_framework import serializers

from .models import Product, Event


class ProductSerializer(serializers.ModelSerializer):

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
            #"participants",
        ]
