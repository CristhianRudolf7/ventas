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
    indicador = serializers.SlugRelatedField(
        slug_field='nombre',
        queryset=Indicador.objects.all()
    )
    trabajador = serializers.SlugRelatedField(
        slug_field='nombre',
        queryset=Trabajador.objects.all()
    )

    class Meta:
        model = Registro
        fields = '__all__'