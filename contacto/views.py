from django.shortcuts import render
from rest_framework.views import APIView
from .models import Contacto
from django.http.response import JsonResponse
from http import HTTPStatus
from .serializer import ContactoSerializer
from utils import utils


class Contacto(APIView):

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
