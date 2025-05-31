from django.contrib import admin
from .models import GrupoArticulo, LineaArticulo, Articulo, ListaPrecio

@admin.register(GrupoArticulo)
class GrupoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre_grupo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['nombre_grupo']
    ordering = ['nombre_grupo']

@admin.register(LineaArticulo)
class LineaArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre_linea', 'grupo', 'estado', 'fecha_creacion']
    list_filter = ['grupo', 'estado', 'fecha_creacion']
    search_fields = ['nombre_linea', 'grupo__nombre_grupo']
    ordering = ['grupo__nombre_grupo', 'nombre_linea']

class ListaPrecioInline(admin.TabularInline):
    model = ListaPrecio
    extra = 0

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo_articulo', 'descripcion', 'grupo', 'linea', 'stock', 'estado']
    list_filter = ['grupo', 'linea', 'estado', 'fecha_creacion']
    search_fields = ['codigo_articulo', 'codigo_barras', 'descripcion']
    ordering = ['codigo_articulo']
    inlines = [ListaPrecioInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_articulo', 'codigo_barras', 'descripcion', 'presentacion')
        }),
        ('Clasificación', {
            'fields': ('grupo', 'linea')
        }),
        ('Inventario', {
            'fields': ('stock', 'estado')
        }),
    )

@admin.register(ListaPrecio)
class ListaPrecioAdmin(admin.ModelAdmin):
    list_display = ['articulo', 'precio_1', 'precio_2', 'precio_compra', 'precio_costo']
    search_fields = ['articulo__descripcion', 'articulo__codigo_articulo']
    ordering = ['articulo__descripcion']