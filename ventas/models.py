import uuid
from django.db import models

class Trabajador(models.Model):
    trabajador_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'Trabajadores'

    def __str__(self):
        return self.nombre

class Indicador(models.Model):
    indicador_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    nombre_indicador = models.CharField(max_length=100)
    meta = models.PositiveIntegerField()
    frecuencia = models.CharField(
        max_length=100, choices=[('D', 'diario'), ('S', 'semanal'), ('M', 'mensual'), ('A', 'anual')],
        default='semanal'
    )
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Indicadores'

    def __str__(self):
        return self.nombre

class Registro(models.Model):
    registro_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField(blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, editable=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, editable=True)

    class Meta:
        db_table = 'Registros'