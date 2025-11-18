from django.urls import path
from .views import *

urlpatterns = [
    path('recetas/editar/foto', Clase1.as_view()),
    path('recetas-panel/<int:id>', Clase4.as_view())
]
