from django.db import models
from autoslug import AutoSlugField
from categorias.models import Categoria


class Receta(models.Model):
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, default=1)
    nombre = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='nombre')
    tiempo = models.CharField(max_length=100, null=True)
    foto = models.CharField(max_length=100, null=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'receta'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
# Create your models here.
