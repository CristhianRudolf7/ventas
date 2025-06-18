from rest_framework import serializers
from .models import Trabajador, Indicador, Registro

class TrabajadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

class MetasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicador
        fields = '__all__'

class RegistrosSerializer(serializers.ModelSerializer):
    indicador = serializers.StringRelatedField()
    trabajador = serializers.StringRelatedField()

    class Meta:
        model = Registro
        fields = '__all__'