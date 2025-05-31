from django.contrib import admin
from .models import GrupoArticulo, Articulo, Venta, DetalleVenta

@admin.register(GrupoArticulo)
class GrupoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'grupo', 'precio', 'stock', 'tiene_stock_bajo', 'activo']
    list_filter = ['grupo', 'activo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre']
    list_editable = ['precio', 'stock']
    
    def tiene_stock_bajo(self, obj):
        return obj.tiene_stock_bajo
    tiene_stock_bajo.boolean = True
    tiene_stock_bajo.short_description = 'Stock Bajo'

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_venta', 'usuario', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['numero_venta', 'usuario__username']
    readonly_fields = ['numero_venta', 'fecha']
    inlines = [DetalleVentaInline]