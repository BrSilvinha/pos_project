# core/urls.py - URLs DE LA APP CORREGIDAS

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='home'),
    
    # Artículos
    path('articulos/', views.articulos_list, name='articulos_list'),
    path('articulos/crear/', views.articulo_create, name='articulo_create'),
    path('articulos/<uuid:articulo_id>/', views.articulo_detail, name='articulo_detail'),
    path('articulos/<uuid:articulo_id>/editar/', views.articulo_edit, name='articulo_edit'),
    path('articulos/<uuid:articulo_id>/eliminar/', views.articulo_delete, name='articulo_delete'),
    
    # Carrito
    path('carrito/', views.cart_detail, name='cart_detail'),
    path('carrito/agregar/<uuid:articulo_id>/', views.cart_add, name='cart_add'),
    path('carrito/eliminar/<uuid:articulo_id>/', views.cart_remove, name='cart_remove'),
    path('carrito/vaciar/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Órdenes
    path('ordenes/', views.order_list, name='order_list'),
    path('orden/<uuid:pedido_id>/', views.order_detail, name='order_detail'),
    path('orden/cancelar/<uuid:pedido_id>/', views.cancel_order, name='cancel_order'),
    
    # PDF
    path('orden/pdf/<uuid:pedido_id>/', views.generate_pdf_order, name='generate_pdf_order'),
    
    # API
    path('api/lineas-por-grupo/<int:grupo_id>/', views.lineas_por_grupo, name='lineas_por_grupo'),
]