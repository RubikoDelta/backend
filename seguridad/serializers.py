from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='username')
    nombre = serializers.CharField(source='first_name')
    correo = serializers.EmailField(source='email')

    def validate_correo(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Correo ya en uso.")
        return value

    class Meta:
        model = User
        fields = ('usuario', 'password', 'correo', 'nombre', 'is_active')


class UserLoginSerializer(serializers.ModelSerializer):
    correo = serializers.EmailField(source='email')
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('correo', 'password')
