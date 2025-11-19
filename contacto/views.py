from django.shortcuts import render
from rest_framework.views import APIView
from .models import Contacto
from django.http.response import JsonResponse
from http import HTTPStatus
from .serializer import ContactoSerializer
from utils import utils

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Contacto(APIView):

    @swagger_auto_schema(
        operation_description="Endpoint para Contacto",
        responses={
            200: "Success",
            400: "Bad Request"
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nombre': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre "),
                'correo': openapi.Schema(type=openapi.TYPE_STRING, description="E-mail"),
                'telefono': openapi.Schema(type=openapi.TYPE_STRING, description="Telefono"),
                'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje"),
            },
            required=['nombre', 'correo', 'telefono', 'mensaje']
        )
    )
    def post(self, request):
        try:
            contactoSerializer = ContactoSerializer(data=request.data)
            contactoSerializer.is_valid(raise_exception=True)
            contactoSerializer.save()
            html = f"""
                <h1>Nuevo mensaje de sitio web</h1>
                
                <ul>
                    <li>Nombre: {request.data['nombre']}</li>
                    <li>E-mail: {request.data['correo']}</li>
                    <li>E-mail: {request.data['correo']}</li>
                </ul>
            """
            utils.sendMail(html, "Prueba correo", request.data['correo'])
        except Exception as e:
            raise e

        return JsonResponse({"Mensaje": "Registro creado exitosamente"}, status=HTTPStatus.CREATED)
