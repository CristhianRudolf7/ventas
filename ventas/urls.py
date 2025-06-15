from django.urls import path
from . import views

urlpatterns = [
    # Trabajadores
    path('trabajadores/', views.TrabajadorListCreate.as_view()),
    path('trabajadores/<uuid:trabajador_id>/', views.TrabajadorDetail.as_view()),
    
    # Ventas
    path('registro/', views.RegistroListCreate.as_view()),
    path('registro/<uuid:id>/', views.RegistroDetail.as_view()),
    
    # Metas
    path('indicador/', views.IndicadorListCreate.as_view()),
    path('indicador/<uuid:id>/', views.IndicadorDetail.as_view()),

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