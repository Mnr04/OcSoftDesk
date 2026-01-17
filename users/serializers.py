from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Validates and serializes user data.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared'
            ]

    def validate_age(self, value):
        """
        Checks if the user is at least 15 years old.
        """
        if value < 15:
            raise serializers.ValidationError("Il faut avoir 15 ans minimum.")
        return value

    def create(self, validated_data):
        """
        Creates a new user securely with a hashed password.
        """
        user = User.objects.create_user(**validated_data)
        return user
