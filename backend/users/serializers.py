from rest_framework import serializers
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    total_kg = serializers.SerializerMethodField()
    total_activities = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "phone_number",
            "total_kg",
            "total_activities",
            # "avatar",
        ]

    def get_total_kg(self, obj):
        return obj.get_total_kg_and_activities()["total_kg"]

    def get_total_activities(self, obj):
        return obj.get_total_kg_and_activities()["total_activities"]

    def validate_first_name(self, value):
        return value.lower().capitalize()

    def validate_last_name(self, value):
        return value.lower().capitalize()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "birth_date",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmptySerializer(serializers.Serializer):
    pass
