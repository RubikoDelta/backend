from django.db import models


class Contacto(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    correo = models.EmailField(null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'contacto'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
