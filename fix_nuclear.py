#!/usr/bin/env python
"""
SOLUCIÓN NUCLEAR para el error RelatedObjectDoesNotExist
Este script elimina TODOS los datos problemáticos y crea un sistema limpio
EJECUTAR: python fix_nuclear.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')

try:
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def nuclear_cleanup():
    """Limpieza nuclear de la base de datos"""
    
    print("🚨 INICIANDO LIMPIEZA NUCLEAR DE LA BASE DE DATOS")
    print("=" * 60)
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los artículos existentes")
    
    try:
        from core.models import (
            Articulo, GrupoArticulo, LineaArticulo, ListaPrecio,
            TipoIdentificacion, CanalCliente, Vendedor
        )
        from pos_project.choices import EstadoEntidades
        from django.db import transaction
        
        with transaction.atomic():
            
            # PASO 1: ELIMINAR TODOS LOS ARTÍCULOS PROBLEMÁTICOS
            print("\n🗑️  PASO 1: Eliminando todos los artículos existentes...")
            articulos_count = Articulo.objects.all().count()
            precios_count = ListaPrecio.objects.all().count()
            
            if articulos_count > 0:
                print(f"  📦 Eliminando {articulos_count} artículos...")
                ListaPrecio.objects.all().delete()
                Articulo.objects.all().delete()
                print(f"  ✅ {articulos_count} artículos eliminados")
                print(f"  ✅ {precios_count} precios eliminados")
            else:
                print("  ✅ No hay artículos que eliminar")
            
            # PASO 2: LIMPIAR Y RECREAR GRUPOS Y LÍNEAS
            print("\n📋 PASO 2: Recreando grupos y líneas...")
            
            # Eliminar grupos y líneas existentes
            LineaArticulo.objects.all().delete()
            GrupoArticulo.objects.all().delete()
            print("  🗑️  Grupos y líneas anteriores eliminados")
            
            # Crear grupos por defecto
            grupos_default = [
                'Electrónicos',
                'Ropa y Calzado',
                'Hogar y Jardín',
                'Deportes',
                'Libros y Medios',
                'Alimentación',
                'Salud y Belleza',
                'General'
            ]
            
            grupos_creados = []
            for nombre_grupo in grupos_default:
                grupo = GrupoArticulo.objects.create(
                    nombre_grupo=nombre_grupo,
                    estado=EstadoEntidades.ACTIVO
                )
                grupos_creados.append(grupo)
                print(f"  ✅ Grupo creado: {nombre_grupo}")
            
            # Crear líneas para cada grupo
            lineas_por_grupo = {
                'Electrónicos': ['Celulares', 'Computadoras', 'Audio', 'Accesorios'],
                'Ropa y Calzado': ['Camisas', 'Pantalones', 'Zapatos', 'Accesorios'],
                'Hogar y Jardín': ['Cocina', 'Baño', 'Dormitorio', 'Jardín'],
                'Deportes': ['Fútbol', 'Basketball', 'Running', 'Fitness'],
                'Libros y Medios': ['Libros', 'Revistas', 'DVDs', 'Juegos'],
                'Alimentación': ['Bebidas', 'Snacks', 'Conservas', 'Frescos'],
                'Salud y Belleza': ['Cuidado Personal', 'Medicamentos', 'Cosméticos'],
                'General': ['General']
            }
            
            for grupo in grupos_creados:
                lineas = lineas_por_grupo.get(grupo.nombre_grupo, ['General'])
                for nombre_linea in lineas:
                    LineaArticulo.objects.create(
                        nombre_linea=nombre_linea,
                        grupo=grupo,
                        estado=EstadoEntidades.ACTIVO
                    )
                    print(f"    ✅ Línea creada: {grupo.nombre_grupo} > {nombre_linea}")
            
            # PASO 3: CREAR DATOS BÁSICOS DEL SISTEMA
            print("\n👤 PASO 3: Verificando datos básicos del sistema...")
            
            # Tipos de identificación
            tipos_id = ['DNI', 'RUC', 'Carnet de Extranjería', 'Pasaporte']
            for tipo in tipos_id:
                obj, created = TipoIdentificacion.objects.get_or_create(
                    nombre_tipo_identificacion=tipo,
                    defaults={'estado': EstadoEntidades.ACTIVO}
                )
                if created:
                    print(f"  ✅ Tipo ID creado: {tipo}")
            
            # Canales de cliente
            canales = ['Presencial', 'Online', 'Telefónico', 'WhatsApp']
            for canal in canales:
                obj, created = CanalCliente.objects.get_or_create(
                    nombre_canal=canal,
                    defaults={'estado': EstadoEntidades.ACTIVO}
                )
                if created:
                    print(f"  ✅ Canal creado: {canal}")
            
            # Vendedor por defecto
            if not Vendedor.objects.exists():
                Vendedor.objects.create(
                    nombres='Vendedor Predeterminado',
                    correo_electronico='vendedor@sistema.com',
                    estado=EstadoEntidades.ACTIVO
                )
                print("  ✅ Vendedor predeterminado creado")
            
            # PASO 4: CREAR ARTÍCULOS DE EJEMPLO SEGUROS
            print("\n📦 PASO 4: Creando artículos de ejemplo...")
            
            # Obtener grupo y línea por defecto
            grupo_general = GrupoArticulo.objects.get(nombre_grupo='General')
            linea_general = LineaArticulo.objects.get(nombre_linea='General', grupo=grupo_general)
            
            articulos_ejemplo = [
                {
                    'codigo_articulo': 'EJEM-001',
                    'descripcion': 'Producto de Ejemplo 1',
                    'precio': 10.00
                },
                {
                    'codigo_articulo': 'EJEM-002', 
                    'descripcion': 'Producto de Ejemplo 2',
                    'precio': 25.50
                },
                {
                    'codigo_articulo': 'EJEM-003',
                    'descripcion': 'Producto de Ejemplo 3', 
                    'precio': 99.99
                }
            ]
            
            for item in articulos_ejemplo:
                articulo = Articulo.objects.create(
                    codigo_articulo=item['codigo_articulo'],
                    descripcion=item['descripcion'],
                    grupo=grupo_general,
                    linea=linea_general,
                    stock=100,
                    estado=EstadoEntidades.ACTIVO
                )
                
                ListaPrecio.objects.create(
                    articulo=articulo,
                    precio_1=item['precio'],
                    estado=EstadoEntidades.ACTIVO
                )
                
                print(f"  ✅ Artículo ejemplo creado: {item['codigo_articulo']}")
        
        # VERIFICACIÓN FINAL
        print("\n🔍 VERIFICACIÓN FINAL:")
        total_grupos = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_lineas = LineaArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_articulos = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_precios = ListaPrecio.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        
        print(f"  📋 Grupos activos: {total_grupos}")
        print(f"  📋 Líneas activas: {total_lineas}")
        print(f"  📦 Artículos activos: {total_articulos}")
        print(f"  💰 Precios configurados: {total_precios}")
        
        # Verificar que NO hay artículos huérfanos
        huerfanos = Articulo.objects.filter(grupo__isnull=True).count()
        huerfanos_linea = Articulo.objects.filter(linea__isnull=True).count()
        
        if huerfanos == 0 and huerfanos_linea == 0:
            print("\n🎉 ¡LIMPIEZA NUCLEAR COMPLETADA EXITOSAMENTE!")
            print("  ✅ Base de datos completamente limpia")
            print("  ✅ Datos básicos creados")
            print("  ✅ Artículos de ejemplo disponibles")
            print("  ✅ CERO artículos huérfanos")
            return True
        else:
            print(f"\n❌ AÚN HAY PROBLEMAS:")
            print(f"  • Artículos sin grupo: {huerfanos}")
            print(f"  • Artículos sin línea: {huerfanos_linea}")
            return False
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LA LIMPIEZA: {e}")
        return False

def create_safe_view():
    """Crear una vista completamente segura"""
    
    print("\n🔧 Creando vista segura...")
    
    safe_view_code = '''
# NUEVA VISTA SEGURA - Reemplazar en views.py
@login_required
def articulo_create(request):
    """Vista 100% segura para crear artículos"""
    
    if request.method == 'POST':
        try:
            # Datos del formulario
            codigo = request.POST.get('codigo_articulo', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            grupo_id = request.POST.get('grupo', '')
            linea_id = request.POST.get('linea', '')
            stock = int(request.POST.get('stock', 0))
            precio = float(request.POST.get('precio_1', 0))
            
            # Validaciones
            if not all([codigo, descripcion, grupo_id, linea_id]):
                messages.error(request, 'Todos los campos obligatorios son requeridos.')
                return redirect('articulo_create')
            
            # Crear artículo
            grupo = GrupoArticulo.objects.get(grupo_id=grupo_id)
            linea = LineaArticulo.objects.get(linea_id=linea_id)
            
            with transaction.atomic():
                articulo = Articulo.objects.create(
                    codigo_articulo=codigo,
                    descripcion=descripcion,
                    grupo=grupo,
                    linea=linea,
                    stock=stock,
                    estado=EstadoEntidades.ACTIVO
                )
                
                ListaPrecio.objects.create(
                    articulo=articulo,
                    precio_1=precio,
                    estado=EstadoEntidades.ACTIVO
                )
                
                messages.success(request, f'Artículo "{codigo}" creado exitosamente.')
                return redirect('articulos_list')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # GET - Solo pasar grupos, NUNCA objetos Articulo
    grupos = list(GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).values('grupo_id', 'nombre_grupo'))
    
    return render(request, 'articulos/crear.html', {
        'grupos': grupos,
        'edit_mode': False,
        'articulo': None  # CRÍTICO: NUNCA pasar objeto Articulo
    })
'''
    
    print("✅ Código de vista segura generado")
    print("📋 INSTRUCCIONES:")
    print("   1. Copia el código de vista segura")
    print("   2. Reemplaza la función articulo_create en views.py")
    print("   3. Guarda el archivo")
    
    return safe_view_code

def main():
    """Función principal"""
    
    print("🚨 SOLUCIÓN NUCLEAR PARA RelatedObjectDoesNotExist")
    print("=" * 60)
    
    respuesta = input("⚠️  ¿Continuar con la limpieza nuclear? (elimina TODOS los artículos) [s/N]: ")
    
    if respuesta.lower() not in ['s', 'si', 'sí', 'yes', 'y']:
        print("❌ Operación cancelada")
        return False
    
    # Ejecutar limpieza nuclear
    if nuclear_cleanup():
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Reemplaza la vista articulo_create con el código seguro")
        print("   2. Reemplaza el template crear.html con la versión segura")
        print("   3. python manage.py runserver")
        print("   4. Visita: http://127.0.0.1:8000/articulos/crear/")
        print("\n🎯 El error RelatedObjectDoesNotExist debería estar eliminado")
        return True
    else:
        print("\n❌ La limpieza nuclear falló")
        return False

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)