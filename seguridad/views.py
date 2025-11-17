from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import Http404, HttpResponseRedirect
from http import HTTPStatus
from .serializers import UserSerializer, UserLoginSerializer
from .models import *
import uuid
import os
from dotenv import load_dotenv
from utils import utils
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta
import time
# Create your views here.


class Clase1(APIView):

    def post(self, request):
        userSerializer = UserSerializer(data=request.data)
        userSerializer.is_valid(raise_exception=True)

        token = uuid.uuid4()
        url = f"{os.getenv('BASE_URL')}api/v1/seguridad/verificacion/{token}"
        try:
            usuario = User.objects.create_user(username=request.data['correo'], password=request.data['password'],
                                               email=request.data['correo'], first_name=request.data['nombre'],
                                               last_name='', is_active=0)
            UserMetadata.objects.create(token=token, user_id=usuario.id)

            html = f"""
            <h3>Verificacion de cuenta</h3>
            Hola {request.data['nombre']} tu registro ha sido exitoso. Para activar tu cuenta haz clic en 
            el siguiente enlace: <br/>
            <a href="{url}">{url}</a>
            <br/>
            {url} 
            """

            utils.sendMail(html, "Verificacion", request.data['correo'])
            # utils.sendMail(html, "Prueba correo", request.data['correo'])
        except Exception as e:
            return JsonResponse({"Estado": "Error", "Mensaje": "Ocurrio un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"Estado": "Ok", "Mensaje": "Registro creado exitosamente"}, status=HTTPStatus.CREATED)


class Clase2(APIView):

    def get(self, request, token):
        if token == None or not token:
            return JsonResponse({"Estado": "Error", "Mensaje": "Recurso no disponible"}, statu=Http404)

        try:
            data = UserMetadata.objects.filter(
                token=token).filter(user__is_active=0).get()

            UserMetadata.objects.filter(token=token)

            UserMetadata.objects.filter(token=token).update(token="")

            User.objects.filter(id=data.user_id).update(is_active=1)

            return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))
        except UserMetadata.DoesNotExist:
            raise Http404


class Clase3(APIView):

    def post(self, request):

        userSerializer = UserLoginSerializer(data=request.data, partial=True)
        userSerializer.is_valid(raise_exception=True)

        try:
            user = User.objects.filter(email=request.data['correo']).get()
        except:
            return JsonResponse({"Estado": "Error", "Mensaje": "Recurso no disponible"})

        auth = authenticate(
            request, username=request.data['correo'], password=request.data['password'])

        if auth is not None:
            fecha = datetime.now()
            tomorrow = fecha + timedelta(days=1)
            fecha_timestamp = int(datetime.timestamp(tomorrow))

            payload = {'id': user.id, 'ISS': os.getenv('BASE_URL'), 'iat': int(
                time.time()), 'exp': int(fecha_timestamp)}

            try:
                token = jwt.encode(
                    payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({'id': user.id, 'nombre': user.first_name, 'token': token})
            except Exception as e:
                return JsonResponse({'Estado': 'Error', 'Mensaje': 'Ocurrio un error inesperado'}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"Estado": "Error", "Mensaje": "Credenciales no validas"}, status=HTTPStatus.BAD_REQUEST)
