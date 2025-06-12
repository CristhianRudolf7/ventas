from rest_framework import serializers
from .models import Trabajadores, Ventas, Metas

class TrabajadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajadores
        fields = ['trabajador_id', 'nombre']

class VentasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventas
        fields = '__all__'

class MetasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metas
        fields = '__all__'

class VentasDashboardSerializer(serializers.ModelSerializer):
    trabajador_nombre = serializers.CharField(source='trabajador.nombre')
    class Meta:
        model = Ventas
        fields = ['venta_id', 'fecha', 'monto', 'cantidad_productos', 'trabajador_nombre']