from rest_framework import serializers
from accounts.models import User


class SchoolAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if not user.is_superuser:
            raise serializers.ValidationError("You must be a superadmin to log in.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        return {'user': user}
