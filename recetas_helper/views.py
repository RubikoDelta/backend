from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from dotenv import load_dotenv
import os
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from recetas.models import *
from categorias.models import Categoria


class Clase1(APIView):

    @logueado()
    def post(self, request):
        if request.data['id'] == None or not request.data['id']:
            return JsonResponse({'Estado': 'Error', 'Mensaje': 'El campo id es obligatorio'})

        try:
            existe = Receta.objects.filter(pk=request.data['id']).get()
            foto_anterior = existe.foto
        except Receta.DoesNotExist:
            return JsonResponse({'Estado': 'Error', 'Mensaje': 'La receta no existe en la Base de datos'}, status=HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"Estado": "Error", "Mensaje": "Debe adjuntar una foto en el campo correspondiente"}, status=HTTPStatus.BAD_REQUEST)

        allowed_type = ["image/jpeg", "image/png"]
        if request.FILES['foto'].content_type not in allowed_type:
            return JsonResponse({"Foto", ["El archivo debe ser una imagen JPG o PNG."]}, status=HTTPStatus.BAD_REQUEST)
        else:
            try:
                fs.save(f"recetas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"Estado": "Error", "Mensaje": "Se produjo un error al intentar subir el archivo"}, status=HTTPStatus.BAD_REQUEST)

            try:
                Receta.objects.filter(id=request.data['id']).update(foto=foto)
                os.remove(f"./uploads/recetas/{foto_anterior}")
                return JsonResponse({"Estado": "Ok", "Mensaje": " Se ha modificado el registro exitosamente"}, status=HTTPStatus.OK)

            except Exception as e:
                return JsonResponse({"Estado": "Error", "Mensaje": "Ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    def get(self, request, slug):
        try:
            data = Receta.objects.filter(slug=slug).get()
            fecha = DateFormat(data.fecha).format('d/m/Y')
            categoria_nombre = data.categoria.nombre
            foto_path = f"{os.getenv('BASE_URL')}uploads/recetas/{data.foto}"
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug,
                                          "tiempo": data.tiempo, "descripcion": data.descripcion, "fecha": fecha,
                                          "categoria_id": data.categoria_id, "categoria": categoria_nombre,
                                          "foto": foto_path, "user_id": data.user_id, "user": data.user.first_name}}, status=HTTPStatus.OK)

        except Receta.DoesNotExist:
            return JsonResponse({"Estado": "Error", "Mensaje": "Recurso no disponible"}, status=HTTPStatus.NOT_FOUND)


class Clase3(APIView):

    def get(self, request):
        data = Receta.objects.order_by('?').all()[:3]
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)


class Clase4(APIView):

    @logueado()
    def get(self, request, id):
        try:
            existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return JsonResponse({"Estado": "Error", "Mensaje": "Ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)

        data = Receta.objects.filter(user_id=id).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)


class Clase5(APIView):

    def get(self, request):
        if request.GET.get("categoria_id") == None or not request.GET.get("categoria_id"):
            return JsonResponse({"Estado": "Error", "Mensaje": "Ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)

        try:
            existe = Categoria.objects.filter(
                id=request.GET.get("categoria_id")).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"Estado": "Error", "Mensaje": "Ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        data = Receta.objects.filter(categoria_id=request.GET.get("categoria_id")).filter(
            nombre__icontains=request.GET.get('search')).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)
