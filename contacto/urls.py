from django.urls import path
from .views import Contacto

urlpatterns = [
    path('contacto', Contacto.as_view()),
]
