from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
# upload
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
# Create your views here.


class Class_Ejemplo(APIView):

    def get(self, request):

        # Metodo con django_rest_framework return HttpResponse(f"Método GET | id={request.query_params.get('id')}")
        return HttpResponse(f"Método GET | id={request.GET.get('id', None)}")


class Class_EjemploParametros(APIView):

    def get(self, request, id):
        return HttpResponse(f"Metodo GET | parametros={id}")

    def put(self, request, id):
        return HttpResponse(f"Metodo PUT | parametros={id}")

    def delete(self, request, id):
        return HttpResponse(f"Metodo DELETE | parametros={id}")


class Class_EjemploUpload(APIView):

    def post(self, request):
        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file']))[1]}"
        fs.save(f"ejemplo/{foto}", request.FILES['file'])
        fs.url(request.FILES['file'])
        return JsonResponse({"estado": "ok", "mensaje": "Se subió el archivo"})
