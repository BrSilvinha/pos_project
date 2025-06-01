#!/usr/bin/env python
"""
Script para corregir problemas en la base de datos del Sistema POS
Ejecutar: python fix_database.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.db import transaction
from core.models import (
    GrupoArticulo, LineaArticulo, Articulo, ListaPrecio,
    TipoIdentificacion, CanalCliente, Vendedor
)
from pos_project.choices import EstadoEntidades

def verificar_y_crear_datos_basicos():
    """Verificar y crear datos básicos del sistema"""
    
    print("🔍 Verificando datos básicos del sistema...")
    
    # 1. Verificar y crear grupos de artículos
    if not GrupoArticulo.objects.exists():
        print("📦 Creando grupos de artículos por defecto...")
        grupos_default = [
            'Electrónicos',
            'Ropa y Accesorios',
            'Hogar y Jardín',
            'Deportes y Aire Libre',
            'Libros y Medios',
            'General'
        ]
        
        for nombre_grupo in grupos_default:
            grupo, created = GrupoArticulo.objects.get_or_create(
                nombre_grupo=nombre_grupo,
                defaults={'estado': EstadoEntidades.ACTIVO}
            )
            if created:
                print(f"  ✅ Grupo creado: {nombre_grupo}")
    
    # 2. Verificar líneas para cada grupo
    grupos = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO)
    for grupo in grupos:
        if not LineaArticulo.objects.filter(grupo=grupo).exists():
            print(f"📋 Creando línea por defecto para grupo: {grupo.nombre_grupo}")
            LineaArticulo.objects.create(
                nombre_linea='General',
                grupo=grupo,
                estado=EstadoEntidades.ACTIVO
            )
    
    # 3. Verificar tipos de identificación
    if not TipoIdentificacion.objects.exists():
        print("🆔 Creando tipos de identificación...")
        tipos = ['DNI', 'RUC', 'Carnet de Extranjería', 'Pasaporte']
        for tipo in tipos:
            TipoIdentificacion.objects.create(
                nombre_tipo_identificacion=tipo,
                estado=EstadoEntidades.ACTIVO
            )
            print(f"  ✅ Tipo creado: {tipo}")
    
    # 4. Verificar canales de cliente
    if not CanalCliente.objects.exists():
        print("📱 Creando canales de cliente...")
        canales = ['Presencial', 'Online', 'Telefónico', 'WhatsApp']
        for canal in canales:
            CanalCliente.objects.create(
                nombre_canal=canal,
                estado=EstadoEntidades.ACTIVO
            )
            print(f"  ✅ Canal creado: {canal}")
    
    # 5. Verificar vendedores
    if not Vendedor.objects.exists():
        print("👤 Creando vendedor por defecto...")
        Vendedor.objects.create(
            nombres='Vendedor Predeterminado',
            correo_electronico='vendedor@sistema.com',
            estado=EstadoEntidades.ACTIVO
        )
        print("  ✅ Vendedor creado")

def corregir_articulos_sin_grupo():
    """Corregir artículos que no tienen grupo asignado"""
    
    print("\n🔧 Verificando artículos sin grupo...")
    
    # Buscar artículos que puedan tener grupo NULL
    try:
        articulos_sin_grupo = Articulo.objects.filter(grupo__isnull=True)
        
        if articulos_sin_grupo.exists():
            print(f"⚠️  Encontrados {articulos_sin_grupo.count()} artículos sin grupo")
            
            # Obtener o crear grupo "General"
            grupo_general, created = GrupoArticulo.objects.get_or_create(
                nombre_grupo='General',
                defaults={'estado': EstadoEntidades.ACTIVO}
            )
            
            # Obtener o crear línea "General" para ese grupo
            linea_general, created = LineaArticulo.objects.get_or_create(
                nombre_linea='General',
                grupo=grupo_general,
                defaults={'estado': EstadoEntidades.ACTIVO}
            )
            
            # Asignar grupo y línea a los artículos
            with transaction.atomic():
                for articulo in articulos_sin_grupo:
                    articulo.grupo = grupo_general
                    articulo.linea = linea_general
                    articulo.save()
                    print(f"  ✅ Artículo corregido: {articulo.codigo_articulo}")
        
        else:
            print("✅ Todos los artículos tienen grupo asignado")
            
    except Exception as e:
        print(f"❌ Error verificando artículos: {e}")

def corregir_articulos_sin_linea():
    """Corregir artículos que no tienen línea asignada"""
    
    print("\n🔧 Verificando artículos sin línea...")
    
    try:
        articulos_sin_linea = Articulo.objects.filter(linea__isnull=True)
        
        if articulos_sin_linea.exists():
            print(f"⚠️  Encontrados {articulos_sin_linea.count()} artículos sin línea")
            
            with transaction.atomic():
                for articulo in articulos_sin_linea:
                    # Buscar una línea para el grupo del artículo
                    linea = LineaArticulo.objects.filter(
                        grupo=articulo.grupo,
                        estado=EstadoEntidades.ACTIVO
                    ).first()
                    
                    if not linea:
                        # Crear línea "General" para el grupo
                        linea = LineaArticulo.objects.create(
                            nombre_linea='General',
                            grupo=articulo.grupo,
                            estado=EstadoEntidades.ACTIVO
                        )
                    
                    articulo.linea = linea
                    articulo.save()
                    print(f"  ✅ Línea asignada a: {articulo.codigo_articulo}")
        
        else:
            print("✅ Todos los artículos tienen línea asignada")
            
    except Exception as e:
        print(f"❌ Error verificando líneas: {e}")

def verificar_precios():
    """Verificar que los artículos tengan precios"""
    
    print("\n💰 Verificando precios de artículos...")
    
    try:
        articulos_sin_precio = []
        
        for articulo in Articulo.objects.filter(estado=EstadoEntidades.ACTIVO):
            if not articulo.precios.exists():
                articulos_sin_precio.append(articulo)
        
        if articulos_sin_precio:
            print(f"⚠️  Encontrados {len(articulos_sin_precio)} artículos sin precio")
            
            for articulo in articulos_sin_precio:
                # Crear precio por defecto
                ListaPrecio.objects.create(
                    articulo=articulo,
                    precio_1=1.00,  # Precio por defecto
                    estado=EstadoEntidades.ACTIVO
                )
                print(f"  ✅ Precio creado para: {articulo.codigo_articulo}")
        
        else:
            print("✅ Todos los artículos activos tienen precios")
            
    except Exception as e:
        print(f"❌ Error verificando precios: {e}")

def mostrar_estadisticas():
    """Mostrar estadísticas del sistema"""
    
    print("\n📊 ESTADÍSTICAS DEL SISTEMA")
    print("=" * 40)
    
    try:
        print(f"👥 Grupos de artículos: {GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"📋 Líneas de artículos: {LineaArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"📦 Artículos activos: {Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"💰 Precios configurados: {ListaPrecio.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"🆔 Tipos de identificación: {TipoIdentificacion.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"📱 Canales de cliente: {CanalCliente.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        print(f"👤 Vendedores: {Vendedor.objects.filter(estado=EstadoEntidades.ACTIVO).count()}")
        
        # Mostrar algunos artículos de ejemplo
        print("\n📦 Artículos de ejemplo:")
        articulos_muestra = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).select_related('grupo', 'linea')[:5]
        for articulo in articulos_muestra:
            print(f"  • {articulo.codigo_articulo} - {articulo.descripcion}")
            print(f"    Grupo: {articulo.grupo.nombre_grupo} | Línea: {articulo.linea.nombre_linea}")
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    """Función principal"""
    
    print("🛠️  SISTEMA POS - CORRECTOR DE BASE DE DATOS")
    print("=" * 50)
    
    try:
        with transaction.atomic():
            # 1. Verificar y crear datos básicos
            verificar_y_crear_datos_basicos()
            
            # 2. Corregir artículos sin grupo
            corregir_articulos_sin_grupo()
            
            # 3. Corregir artículos sin línea
            corregir_articulos_sin_linea()
            
            # 4. Verificar precios
            verificar_precios()
        
        # 5. Mostrar estadísticas
        mostrar_estadisticas()
        
        print("\n🎉 ¡Base de datos corregida exitosamente!")
        print("\n📋 Ahora puedes ejecutar:")
        print("   python manage.py runserver")
        print("   Y visitar: http://127.0.0.1:8000/articulos/crear/")
        
    except Exception as e:
        print(f"\n❌ Error durante la corrección: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()