from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from .serializers import RecetaSerializer
from .models import Receta
# Create your views here.


class Clase1(APIView):
    def get(self, request):
        data = Receta.objects.order_by('-id').all()
        dato_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": dato_json.data})
