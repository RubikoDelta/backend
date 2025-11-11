from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home_inicio(self, request):
    return HttpResponse("Hola mundo")
