# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard - también accesible como 'home'
    path('', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),  # ← AGREGAR ESTA LÍNEA
    
    # Artículos
    path('articulos/', views.articulos_list, name='articulos_list'),
    path('articulos/crear/', views.articulo_create, name='articulo_create'),
    path('articulos/<int:pk>/', views.articulo_detail, name='articulo_detail'),
    path('articulos/<int:pk>/editar/', views.articulo_edit, name='articulo_edit'),
    path('articulos/<int:pk>/eliminar/', views.articulo_delete, name='articulo_delete'),
    
    # API endpoints
    path('api/lineas-por-grupo/<int:grupo_id>/', views.lineas_por_grupo, name='lineas_por_grupo'),
]