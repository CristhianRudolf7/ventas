from django.urls import path
from . import views

urlpatterns = [
    # Trabajadores
    path('trabajadores/', views.TrabajadorListCreate.as_view()),
    path('trabajadores/<uuid:trabajador_id>/', views.TrabajadorDetail.as_view()),
    
    # Ventas
    path('registros/', views.RegistroListCreate.as_view()),
    path('registros/<uuid:registro_id>/', views.RegistroDetail.as_view()),
    
    # Metas
    path('indicadores/', views.IndicadorListCreate.as_view()),
    path('indicadores/<uuid:indicador_id>/', views.IndicadorDetail.as_view()),
    path('indicadores/ventas/', views.IndicadorVentasView.as_view(), name='indicador_ventas'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]

'''
trabajadores
indicadores
registros a partir de la id de un indicador = meta
permitir registrar un indicador = meta
borrar un indicador
permitir insertar un registro en un indicador a partir de la id
urls para eliminar
'''