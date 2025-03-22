from rest_framework import serializers
from django.contrib.auth import get_user_model

# from .models import User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
        ]

    def validate_first_name(self, value):
        """Ensure the first name contains only letters."""
        # if not value.isalpha():
        #    raise serializers.ValidationError("First name must contain only letters.")
        return value.lower().capitalize()

    def validate_last_name(self, value):
        """Ensure the last name contains only letters."""
        # if not value.isalpha():
        #    raise serializers.ValidationError("Last name must contain only letters.")
        return value.lower().capitalize()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "birth_date", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
