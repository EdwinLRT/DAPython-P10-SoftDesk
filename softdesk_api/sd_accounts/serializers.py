from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'age', 'can_be_contacted', 'can_data_be_shared']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")
        return value