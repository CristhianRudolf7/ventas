import uuid
from django.db import models

class Trabajadores(models.Model):
    trabajador_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Trabajadores'
        verbose_name_plural = 'Trabajadores'

class Ventas(models.Model):
    venta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_productos = models.PositiveIntegerField()
    trabajador = models.ForeignKey(Trabajadores, on_delete=models.CASCADE, editable=False)

    class Meta:
        db_table = 'Ventas'
        ordering = ['fecha']

class Metas(models.Model):
    metas_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    cantidad_meta = models.PositiveIntegerField()

    class Meta:
        db_table = 'Metas'