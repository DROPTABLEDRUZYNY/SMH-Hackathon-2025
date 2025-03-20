from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "sex",
        ]

    def validate_first_name(self, value):
        """Ensure the first name contains only letters."""
        #if not value.isalpha():
        #    raise serializers.ValidationError("First name must contain only letters.")
        return value.lower().capitalize()

    def validate_last_name(self, value):
        """Ensure the last name contains only letters."""
        #if not value.isalpha():
        #    raise serializers.ValidationError("Last name must contain only letters.")
        return value.lower().capitalize()
