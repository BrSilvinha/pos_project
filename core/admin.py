from django.contrib import admin
from .models import (
    Usuario, GrupoArticulo, LineaArticulo, Articulo, ListaPrecio,
    TipoIdentificacion, CanalCliente, Cliente, Vendedor,
    OrdenCompraCliente, ItemOrdenCompraCliente
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'full_name']

@admin.register(GrupoArticulo)
class GrupoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre_grupo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['nombre_grupo']

@admin.register(LineaArticulo)
class LineaArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre_linea', 'grupo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'grupo', 'fecha_creacion']
    search_fields = ['nombre_linea', 'grupo__nombre_grupo']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo_articulo', 'descripcion', 'grupo', 'linea', 'stock', 'estado']
    list_filter = ['estado', 'grupo', 'linea', 'fecha_creacion']
    search_fields = ['codigo_articulo', 'descripcion', 'codigo_barras']
    list_editable = ['stock']

@admin.register(ListaPrecio)
class ListaPrecioAdmin(admin.ModelAdmin):
    list_display = ['articulo', 'precio_1', 'precio_2', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['articulo__descripcion', 'articulo__codigo_articulo']

@admin.register(TipoIdentificacion)
class TipoIdentificacionAdmin(admin.ModelAdmin):
    list_display = ['nombre_tipo_identificacion', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre_tipo_identificacion']

@admin.register(CanalCliente)
class CanalClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_canal', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre_canal']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'nro_documento', 'correo_electronico', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'tipo_identificacion', 'canal', 'fecha_creacion']
    search_fields = ['nombres', 'nro_documento', 'correo_electronico']

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'correo_electronico', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['nombres', 'correo_electronico']

@admin.register(OrdenCompraCliente)
class OrdenCompraClienteAdmin(admin.ModelAdmin):
    list_display = ['nro_pedido', 'cliente', 'vendedor', 'importe', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion', 'fecha_pedido']
    search_fields = ['nro_pedido', 'cliente__nombres', 'vendedor__nombres']
    readonly_fields = ['pedido_id', 'nro_pedido', 'importe']

@admin.register(ItemOrdenCompraCliente)
class ItemOrdenCompraClienteAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'articulo', 'cantidad', 'precio_unitario', 'total_item']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['pedido__nro_pedido', 'articulo__descripcion']
    readonly_fields = ['item_id', 'total_item']