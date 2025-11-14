from datetime import datetime
from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from .serializers import RecetaSerializer
from .models import Receta
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


class Clase1(APIView):
    def get(self, request):
        data = Receta.objects.order_by('-id').all()
        dato_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": dato_json.data})

    def post(self, request):
        try:
            recetaSerializer = RecetaSerializer(data=request.data)
            recetaSerializer.is_valid(raise_exception=True)

            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
            fs = FileSystemStorage()
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"Estado": "Error", "Mensaje": "Se produjo un error al intentar subir la foto"}, status=HTTPStatus.BAD_REQUEST)

            Receta.objects.create(nombre=request.data['nombre'], tiempo=request.data['tiempo'], descripcion=request.data['descripcion'],
                                  categoria_id=request.data['categoria_id'], foto=foto)

            return JsonResponse({"estado": "ok", "mensaje": "Se crea el registro exitosamente"})
        except Exception as e:
            raise e


class Clase2(APIView):

    def get(self, request, id):
        try:
            data = Receta.objects.filter(id=id).get()
            fecha = DateFormat(data.fecha).format('d/m/Y')
            categoria_nombre = data.categoria.nombre
            foto_path = f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}"
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug,
                                          "tiempo": data.tiempo, "descripcion": data.descripcion, "fecha": fecha,
                                          "categoria_id": data.categoria_id, "categoria": categoria_nombre,
                                          "foto": foto_path}}, status=HTTPStatus.OK)
        except Receta.DoesNotExist:
            return JsonResponse({"Estado": "Error", "Mensaje": "Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)
