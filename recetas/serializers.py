from rest_framework import serializers

from .models import Categoria
from .models import Receta
from dotenv import load_dotenv
from datetime import datetime
import os


class RecetaSerializer(serializers.ModelSerializer):
    categoria = serializers.ReadOnlyField(source='categoria.nombre')
    fecha = serializers.DateTimeField(
        format="%d/%m/%Y", read_only=True)
    foto = serializers.FileField(required=True)
    foto_url = serializers.SerializerMethodField(read_only=True)
    categoria_id = serializers.IntegerField()

    def validate_categoria_id(self, value):
        if not Categoria.objects.filter(pk=value).exists():
            raise serializers.ValidationError("La categoría no existe.")
        return value

    def validate_foto(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise serializers.ValidationError(
                "El archivo debe ser una imagen válida.")
        return value

    class Meta:
        model = Receta
        fields = ("id", "nombre", "slug", "tiempo", "descripcion",
                  "fecha", "categoria", "categoria_id", "foto", "foto_url")

    def get_foto_url(self, obj):
        return f"{os.getenv('BASE_URL')}uploads/recetas/{obj.foto}"
