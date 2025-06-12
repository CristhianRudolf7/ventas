from rest_framework import generics
from .models import Trabajadores, Ventas, Metas
from .serializers import TrabajadoresSerializer, VentasSerializer, MetasSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Max
from rest_framework.views import APIView
from rest_framework.response import Response

class DashboardView(APIView):
    def get(self, request):
        # 1. Trabajador con más ventas (por monto total)
        trabajador_top = Trabajadores.objects.annotate(
            total_ventas=Sum('ventas__monto'),
            num_ventas=Count('ventas')
        ).order_by('-total_ventas').first()

        # 2. Distribución de productos por venta
        distribucion_productos = Ventas.objects.values('cantidad_productos').annotate(
            total=Count('venta_id')
        ).order_by('cantidad_productos')

        # 3. Total de ventas hoy
        hoy = timezone.now().date()
        ventas_hoy = Ventas.objects.filter(fecha__date=hoy).aggregate(
            total=Sum('monto'),
            cantidad=Count('venta_id')
        )

        # 4. Meta del mes actual vs ventas reales
        hoy = timezone.now()
        inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        meta_mes = Metas.objects.filter(
            fecha_inicio__lte=fin_mes,
            fecha_fin__gte=inicio_mes
        ).first()
        
        ventas_mes = Ventas.objects.filter(
            fecha__range=(inicio_mes, fin_mes)
        ).aggregate(total=Sum('monto'))['total'] or 0

        # 5. Últimas 5 ventas registradas
        ultimas_ventas = Ventas.objects.select_related('trabajador').order_by('-fecha')[:5]

        # 6. Evolución diaria de ventas (últimos 7 días)
        fecha_limite = hoy - timedelta(days=7)
        evolucion_ventas = Ventas.objects.filter(
            fecha__date__gte=fecha_limite
        ).values('fecha__date').annotate(
            total=Sum('monto')
        ).order_by('fecha__date')

        # Estructura de respuesta
        data = {
            "trabajador_top": {
                "id": str(trabajador_top.trabajador_id),
                "nombre": trabajador_top.nombre,
                "total_ventas": float(trabajador_top.total_ventas),
                "num_ventas": trabajador_top.num_ventas
            } if trabajador_top else None,
            
            "distribucion_productos": list(distribucion_productos),
            
            "ventas_hoy": {
                "total": float(ventas_hoy['total'] or 0),
                "cantidad": ventas_hoy['cantidad'] or 0
            },
            
            "meta_mes": {
                "meta_id": str(meta_mes.metas_id),
                "objetivo": meta_mes.cantidad_meta,
                "alcanzado": float(ventas_mes),
                "porcentaje": min(100, round((ventas_mes / meta_mes.cantidad_meta) * 100, 2)) if meta_mes else 0
            } if meta_mes else None,
            
            "ultimas_ventas": [
                {
                    "id": str(v.venta_id),
                    "fecha": v.fecha,
                    "monto": float(v.monto),
                    "productos": v.cantidad_productos,
                    "trabajador": v.trabajador.nombre
                } for v in ultimas_ventas
            ],
            
            "evolucion_ventas": [
                {
                    "fecha": item['fecha__date'].strftime("%Y-%m-%d"),
                    "total": float(item['total'] or 0)
                } for item in evolucion_ventas
            ]
        }

        return Response(data)
    
# Trabajadores
class TrabajadorListCreate(generics.ListCreateAPIView):
    queryset = Trabajadores.objects.all()
    serializer_class = TrabajadoresSerializer

class TrabajadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trabajadores.objects.all()
    serializer_class = TrabajadoresSerializer
    lookup_field = 'trabajador_id'

# Ventas
class VentaListCreate(generics.ListCreateAPIView):
    queryset = Ventas.objects.all()
    serializer_class = VentasSerializer

class VentaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ventas.objects.all()
    serializer_class = VentasSerializer
    lookup_field = 'venta_id'

# Metas
class MetaListCreate(generics.ListCreateAPIView):
    queryset = Metas.objects.all()
    serializer_class = MetasSerializer

class MetaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Metas.objects.all()
    serializer_class = MetasSerializer
    lookup_field = 'metas_id'