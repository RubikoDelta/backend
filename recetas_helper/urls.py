from django.urls import path
from .views import *

urlpatterns = [
    path('recetas-panel/<int:id>', Clase4.as_view())
]
