from rest_framework import serializers
from datetime import datetime
from .models import Contacto


class ContactoSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(
        format="%d%m%Y", read_only=True
    )

    class Meta:
        model = Contacto
        fields = ('id', 'nombre', 'correo', 'telefono', 'mensaje', 'fecha')
