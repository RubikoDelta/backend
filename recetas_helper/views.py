from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from recetas.models import *


class Clase1(APIView):

    def get(APIView):
        pass


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
