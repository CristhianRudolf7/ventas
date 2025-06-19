from rest_framework import generics
from .models import Trabajador, Indicador, Registro
from .serializers import TrabajadoresSerializer, MetasSerializer, RegistrosSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Max
from rest_framework.views import APIView
from rest_framework.response import Response

class DashboardView(APIView):
    def get(self, request):
        # 1. Trabajador con más registros (por cantidad total)
        trabajador_top = Trabajador.objects.annotate(
            total_registros=Sum('registro__cantidad'),
            num_registros=Count('registro')
        ).order_by('-total_registros').first()

        # 2. Distribución de registros por cantidad
        distribucion_registros = Registro.objects.values('cantidad').annotate(
            total=Count('registro_id')
        ).order_by('cantidad')

        # 3. Total de registros hoy
        hoy = timezone.now().date()
        registros_hoy = Registro.objects.filter(fecha__date=hoy).aggregate(
            total=Sum('cantidad'),
            cantidad=Count('registro_id')
        )

        # 4. Indicador del mes actual vs registros reales
        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        indicador_mes = Indicador.objects.filter(
            fecha_inicio__lte=fin_mes,
            activo=True
        ).first()

        registros_mes = Registro.objects.filter(
            fecha__range=(inicio_mes, fin_mes),
            indicador=indicador_mes
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        # 5. Últimos 5 registros
        ultimos_registros = Registro.objects.select_related('trabajador').order_by('-fecha')[:5]

        # 6. Evolución diaria de registros (últimos 7 días)
        fecha_limite = hoy - timedelta(days=7)
        evolucion_registros = Registro.objects.filter(
            fecha__date__gte=fecha_limite
        ).values('fecha__date').annotate(
            total=Sum('cantidad')
        ).order_by('fecha__date')

        # 7. Indicadores basados en registros
        indicadores_activos = Indicador.objects.filter(
            fecha_inicio__lte=fin_mes,
            activo=True
        )

        indicadores_data = []
        for indicador in indicadores_activos:
            registros_total = Registro.objects.filter(
                fecha__range=(inicio_mes, fin_mes),
                indicador=indicador
            ).aggregate(total=Sum('cantidad'))['total'] or 0

            porcentaje = min(100, round((registros_total / indicador.meta) * 100, 2)) if indicador.meta > 0 else 0

            indicadores_data.append({
                "indicador_id": str(indicador.indicador_id),
                "nombre": indicador.nombre,
                "objetivo": indicador.meta,
                "alcanzado": registros_total,
                "porcentaje": porcentaje
            })

        data = {
            "trabajador_top": {
                "id": str(trabajador_top.trabajador_id),
                "nombre": trabajador_top.nombre,
                "total_registros": int(trabajador_top.total_registros),
                "num_registros": trabajador_top.num_registros
            } if trabajador_top else None,

            "distribucion_registros": list(distribucion_registros),

            "registros_hoy": {
                "total": int(registros_hoy['total'] or 0),
                "cantidad": registros_hoy['cantidad'] or 0
            },

            "indicador_mes": {
                "indicador_id": str(indicador_mes.indicador_id),
                "objetivo": indicador_mes.meta,
                "alcanzado": int(registros_mes),
                "porcentaje": min(100, round((registros_mes / indicador_mes.meta) * 100, 2)) if indicador_mes else 0
            } if indicador_mes else None,

            "ultimos_registros": [
                {
                    "id": str(r.registro_id),
                    "fecha": r.fecha,
                    "cantidad": r.cantidad,
                    "trabajador": r.trabajador.nombre
                } for r in ultimos_registros
            ],

            "evolucion_registros": [
                {
                    "fecha": item['fecha__date'].strftime("%Y-%m-%d"),
                    "total": int(item['total'] or 0)
                } for item in evolucion_registros
            ],

            "indicadores": indicadores_data
        }

        return Response(data)

class TrabajadorListCreate(generics.ListCreateAPIView):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadoresSerializer

class TrabajadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadoresSerializer
    lookup_field = 'trabajador_id'

class IndicadorListCreate(generics.ListCreateAPIView):
    queryset = Indicador.objects.all()
    serializer_class = MetasSerializer

class IndicadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Indicador.objects.all()
    serializer_class = MetasSerializer
    lookup_field = 'indicador_id'

class RegistroListCreate(generics.ListCreateAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistrosSerializer

class RegistroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registro.objects.all()
    serializer_class = RegistrosSerializer
    lookup_field = 'registro_id'