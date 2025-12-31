from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'age', 'can_be_contacted', 'can_data_be_shared']

    def validate_age(self, value):
        """
        django validate age automatically
        """
        if value < 15:
            raise serializers.ValidationError("Il faut avoir 15 ans minimum.")
        return value

    def create(self, validated_data):
        """
        Creates a new user and hashes the password for security.
        """
        user = User.objects.create_user(**validated_data)
        return user