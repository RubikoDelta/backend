from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from recetas.models import *


class Clase1(APIView):

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
