# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),
    
    # Artículos
    path('articulos/', views.articulos_list, name='articulos_list'),
    path('articulos/<uuid:articulo_id>/', views.articulo_detail, name='articulo_detail'),
    
    # Carrito
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<uuid:articulo_id>/', views.cart_add, name='cart_add'),
    path('carrito/eliminar/<uuid:articulo_id>/', views.cart_remove, name='cart_remove'),
    path('carrito/vaciar/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
    path('orden/<uuid:pedido_id>/', views.order_detail, name='order_detail'),
    
    # API endpoints
    path('api/lineas-por-grupo/<int:grupo_id>/', views.lineas_por_grupo, name='lineas_por_grupo'),
]