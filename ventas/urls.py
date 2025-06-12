from django.urls import path
from . import views

urlpatterns = [
    # Trabajadores
    path('trabajadores/', views.TrabajadorListCreate.as_view()),
    path('trabajadores/<uuid:trabajador_id>/', views.TrabajadorDetail.as_view()),
    
    # Ventas
    path('ventas/', views.VentaListCreate.as_view()),
    path('ventas/<uuid:venta_id>/', views.VentaDetail.as_view()),
    
    # Metas
    path('metas/', views.MetaListCreate.as_view()),
    path('metas/<uuid:metas_id>/', views.MetaDetail.as_view()),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]