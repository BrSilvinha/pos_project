#!/usr/bin/env python
"""
Script de emergencia para corregir el error RelatedObjectDoesNotExist
Ejecutar: python fix_emergency.py
"""

import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')

try:
    import django
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def fix_immediate():
    """Solución inmediata al problema"""
    
    print("🚨 SOLUCIÓN INMEDIATA AL ERROR RelatedObjectDoesNotExist")
    print("=" * 60)
    
    try:
        from core.models import GrupoArticulo, LineaArticulo, Articulo
        from pos_project.choices import EstadoEntidades
        
        # 1. Crear grupo por defecto si no existe
        print("📦 Creando grupo por defecto...")
        grupo_general, created = GrupoArticulo.objects.get_or_create(
            nombre_grupo='General',
            defaults={'estado': EstadoEntidades.ACTIVO}
        )
        if created:
            print("  ✅ Grupo 'General' creado")
        else:
            print("  ✅ Grupo 'General' ya existe")
        
        # 2. Crear línea por defecto para el grupo
        print("📋 Creando línea por defecto...")
        linea_general, created = LineaArticulo.objects.get_or_create(
            nombre_linea='General',
            grupo=grupo_general,
            defaults={'estado': EstadoEntidades.ACTIVO}
        )
        if created:
            print("  ✅ Línea 'General' creada")
        else:
            print("  ✅ Línea 'General' ya existe")
        
        # 3. Contar artículos problemáticos
        articulos_sin_grupo = Articulo.objects.filter(grupo__isnull=True).count()
        articulos_sin_linea = Articulo.objects.filter(linea__isnull=True).count()
        
        print(f"\n🔍 Diagnóstico:")
        print(f"  • Artículos sin grupo: {articulos_sin_grupo}")
        print(f"  • Artículos sin línea: {articulos_sin_linea}")
        
        # 4. Corregir artículos sin grupo
        if articulos_sin_grupo > 0:
            print(f"\n🔧 Corrigiendo {articulos_sin_grupo} artículos sin grupo...")
            Articulo.objects.filter(grupo__isnull=True).update(grupo=grupo_general)
            print("  ✅ Artículos sin grupo corregidos")
        
        # 5. Corregir artículos sin línea
        if articulos_sin_linea > 0:
            print(f"\n🔧 Corrigiendo {articulos_sin_linea} artículos sin línea...")
            Articulo.objects.filter(linea__isnull=True).update(linea=linea_general)
            print("  ✅ Artículos sin línea corregidos")
        
        # 6. Crear otros datos básicos si faltan
        print("\n📋 Verificando otros datos básicos...")
        
        from core.models import TipoIdentificacion, CanalCliente, Vendedor
        
        # Tipos de identificación
        if not TipoIdentificacion.objects.exists():
            TipoIdentificacion.objects.create(
                nombre_tipo_identificacion='DNI',
                estado=EstadoEntidades.ACTIVO
            )
            print("  ✅ Tipo de identificación 'DNI' creado")
        
        # Canales de cliente
        if not CanalCliente.objects.exists():
            CanalCliente.objects.create(
                nombre_canal='Presencial',
                estado=EstadoEntidades.ACTIVO
            )
            print("  ✅ Canal 'Presencial' creado")
        
        # Vendedores
        if not Vendedor.objects.exists():
            Vendedor.objects.create(
                nombres='Vendedor Predeterminado',
                correo_electronico='vendedor@sistema.com',
                estado=EstadoEntidades.ACTIVO
            )
            print("  ✅ Vendedor predeterminado creado")
        
        # 7. Verificación final
        print("\n📊 VERIFICACIÓN FINAL:")
        total_grupos = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_lineas = LineaArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_articulos = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        
        print(f"  • Grupos activos: {total_grupos}")
        print(f"  • Líneas activas: {total_lineas}")
        print(f"  • Artículos activos: {total_articulos}")
        
        # Verificar que no hay artículos huérfanos
        huerfanos_grupo = Articulo.objects.filter(grupo__isnull=True).count()
        huerfanos_linea = Articulo.objects.filter(linea__isnull=True).count()
        
        if huerfanos_grupo == 0 and huerfanos_linea == 0:
            print("\n🎉 ¡PROBLEMA SOLUCIONADO!")
            print("  ✅ Todos los artículos tienen grupo y línea asignados")
            print("  ✅ Datos básicos creados exitosamente")
            print("\n📋 Ahora puedes:")
            print("  1. python manage.py runserver")
            print("  2. Visitar: http://127.0.0.1:8000/articulos/crear/")
        else:
            print(f"\n⚠️  Aún hay problemas:")
            print(f"  • Artículos sin grupo: {huerfanos_grupo}")
            print(f"  • Artículos sin línea: {huerfanos_linea}")
            
    except Exception as e:
        print(f"\n❌ Error durante la corrección: {e}")
        print("🔧 Solución alternativa:")
        print("  1. Elimina la carpeta: core/migrations/ (excepto __init__.py)")
        print("  2. python manage.py makemigrations core")
        print("  3. python manage.py migrate")
        print("  4. python create_initial_user.py")
        return False
    
    return True

if __name__ == '__main__':
    try:
        success = fix_immediate()
        if success:
            print("\n🎯 ¡Corrección completada con éxito!")
        else:
            print("\n⚠️  Se requiere intervención manual")
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("\n📞 Si el problema persiste:")
        print("  1. Verifica que estés en el directorio correcto del proyecto")
        print("  2. Verifica que el entorno virtual esté activado")
        print("  3. Ejecuta: python manage.py shell")
        print("  4. Luego: from core.models import *")