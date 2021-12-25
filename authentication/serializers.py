from rest_framework import serializers
from .models import User


class VendorCreateSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username only contains alpha newmeric character')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_vendor(**validated_data)
        return user
