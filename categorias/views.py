from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.response import Response
from .models import Categoria
from .serializers import CategoriaSerializer
from http import HTTPStatus
from django.utils.text import slugify


class Clase1(APIView):
    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        datos_json = CategoriaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get("nombre") == None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Categoria.objects.create(nombre=request.data['nombre'])
            return JsonResponse({"Estado": "Ok", "Mensaje": "Se crea el registro exitosamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404


class Clase2(APIView):
    def get(self, request, id):
        try:
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({"data": {"id": data.id, "nombre": data.nombre, "slug": data.slug}}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404

    def put(self, request, id):
        if request.data.get("nombre") == None or not request.data.get("nombre"):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            data = Categoria.objects.filter(pk=id).get()
            nombre = request.data.get("nombre")
            Categoria.objects.filter(pk=id).update(
                nombre=nombre, slug=slugify(nombre))
            return JsonResponse({"estado": "ok", "mensaje": "Registro modificado exitosamente"}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        try:
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(pk=id).delete()
            return JsonResponse({"Estado": "Ok", "Mensaje": "Se ha eliminado correctamente el registro"}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404

# Create your views here.
