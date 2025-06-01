# create_initial_user.py
# Script para crear un usuario inicial y datos básicos

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from core.models import (
    Usuario, TipoIdentificacion, CanalCliente, Vendedor, 
    GrupoArticulo, LineaArticulo
)

def crear_usuario_admin():
    """Crear usuario administrador inicial"""
    print("=== CREANDO USUARIO ADMINISTRADOR ===")
    
    try:
        # Verificar si ya existe un superusuario
        if Usuario.objects.filter(is_superuser=True).exists():
            print("Ya existe un superusuario en el sistema.")
            return True
        
        # Crear superusuario
        admin_user = Usuario.objects.create_superuser(
            username='admin',
            email='admin@sistemapos.com',
            password='admin123',
            full_name='Administrador del Sistema'
        )
        
        print(f"✅ Usuario administrador creado:")
        print(f"   Usuario: admin")
        print(f"   Contraseña: admin123")
        print(f"   Email: admin@sistemapos.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        return False

def crear_datos_basicos():
    """Crear datos básicos necesarios para el sistema"""
    print("\n=== CREANDO DATOS BÁSICOS ===")
    
    try:
        # Crear tipos de identificación
        if not TipoIdentificacion.objects.exists():
            TipoIdentificacion.objects.create(
                nombre_tipo_identificacion='DNI',
                estado=1
            )
            TipoIdentificacion.objects.create(
                nombre_tipo_identificacion='RUC',
                estado=1
            )
            TipoIdentificacion.objects.create(
                nombre_tipo_identificacion='Pasaporte',
                estado=1
            )
            print("✅ Tipos de identificación creados")
        
        # Crear canales de cliente
        if not CanalCliente.objects.exists():
            CanalCliente.objects.create(
                nombre_canal='Presencial',
                estado=1
            )
            CanalCliente.objects.create(
                nombre_canal='Online',
                estado=1
            )
            CanalCliente.objects.create(
                nombre_canal='Teléfono',
                estado=1
            )
            print("✅ Canales de cliente creados")
        
        # Crear vendedor predeterminado
        if not Vendedor.objects.exists():
            Vendedor.objects.create(
                nombres='Vendedor General',
                correo_electronico='ventas@sistemapos.com',
                estado=1
            )
            print("✅ Vendedor predeterminado creado")
        
        # Crear grupos y líneas de artículos
        if not GrupoArticulo.objects.exists():
            # Grupo General
            grupo_general = GrupoArticulo.objects.create(
                nombre_grupo='General',
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='General',
                grupo=grupo_general,
                estado=1
            )
            
            # Grupo Electrónicos
            grupo_electronicos = GrupoArticulo.objects.create(
                nombre_grupo='Electrónicos',
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Smartphones',
                grupo=grupo_electronicos,
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Laptops',
                grupo=grupo_electronicos,
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Accesorios',
                grupo=grupo_electronicos,
                estado=1
            )
            
            # Grupo Ropa
            grupo_ropa = GrupoArticulo.objects.create(
                nombre_grupo='Ropa y Calzado',
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Ropa Masculina',
                grupo=grupo_ropa,
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Ropa Femenina',
                grupo=grupo_ropa,
                estado=1
            )
            LineaArticulo.objects.create(
                nombre_linea='Calzado',
                grupo=grupo_ropa,
                estado=1
            )
            
            print("✅ Grupos y líneas de artículos creados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos básicos: {e}")
        return False

def mostrar_estadisticas():
    """Mostrar estadísticas del sistema"""
    print("\n=== ESTADÍSTICAS DEL SISTEMA ===")
    
    try:
        stats = {
            'Usuarios': Usuario.objects.count(),
            'Tipos de ID': TipoIdentificacion.objects.count(),
            'Canales': CanalCliente.objects.count(),
            'Vendedores': Vendedor.objects.count(),
            'Grupos': GrupoArticulo.objects.count(),
            'Líneas': LineaArticulo.objects.count(),
        }
        
        for categoria, cantidad in stats.items():
            print(f"  {categoria}: {cantidad}")
        
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")

def main():
    print("CONFIGURACIÓN INICIAL DEL SISTEMA POS")
    print("="*50)
    
    # Crear usuario administrador
    if not crear_usuario_admin():
        print("\n❌ Error creando usuario administrador")
        return
    
    # Crear datos básicos
    if not crear_datos_basicos():
        print("\n❌ Error creando datos básicos")
        return
    
    # Mostrar estadísticas
    mostrar_estadisticas()
    
    print("\n" + "="*50)
    print("✅ CONFIGURACIÓN INICIAL COMPLETADA")
    print("\nPuedes iniciar sesión con:")
    print("  Usuario: admin")
    print("  Contraseña: admin123")
    print("\nPara acceder al sistema, ve a: http://127.0.0.1:8000/login/")
    print("="*50)

if __name__ == '__main__':
    main()