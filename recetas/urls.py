from django.urls import path
from .views import *

urlpatterns = [
    path('recetas', Clase1.as_view())
]
