from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'age', 'can_be_contacted', 'can_data_be_shared']


    # def to_representation(self, instance):
    #     # Exclure le champ 'password' lors de la sérialisation des données
    #     data = super().to_representation(instance)
    #     data.pop('password', None)
    #     return data