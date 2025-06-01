#!/usr/bin/env python
"""
Script para crear datos iniciales del sistema POS
Ejecutar después de las migraciones: python create_initial_user.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import (
    TipoIdentificacion, CanalCliente, Vendedor, 
    GrupoArticulo, LineaArticulo, Usuario
)

def create_initial_data():
    """Crear datos iniciales del sistema"""
    
    print("🚀 Creando datos iniciales del Sistema POS...")
    
    # 1. Crear usuario administrador
    Usuario = get_user_model()
    if not Usuario.objects.filter(username='admin').exists():
        admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@sistema.com',
            password='admin123',
            full_name='Administrador del Sistema',
            is_staff=True,
            is_superuser=True
        )
        print("✅ Usuario administrador creado: admin / admin123")
    else:
        print("⚠️  Usuario administrador ya existe")
    
    # 2. Crear tipos de identificación
    tipos_id = [
        'DNI',
        'RUC',
        'Carnet de Extranjería',
        'Pasaporte'
    ]
    
    for tipo in tipos_id:
        obj, created = TipoIdentificacion.objects.get_or_create(
            nombre_tipo_identificacion=tipo,
            defaults={'estado': 1}
        )
        if created:
            print(f"✅ Tipo de identificación creado: {tipo}")
    
    # 3. Crear canales de cliente
    canales = [
        'Presencial',
        'Online',
        'Telefónico',
        'WhatsApp'
    ]
    
    for canal in canales:
        obj, created = CanalCliente.objects.get_or_create(
            nombre_canal=canal,
            defaults={'estado': 1}
        )
        if created:
            print(f"✅ Canal de cliente creado: {canal}")
    
    # 4. Crear vendedor predeterminado
    if not Vendedor.objects.exists():
        vendedor = Vendedor.objects.create(
            nombres='Vendedor Predeterminado',
            correo_electronico='vendedor@sistema.com',
            estado=1
        )
        print("✅ Vendedor predeterminado creado")
    
    # 5. Crear grupos y líneas de artículos
    grupos_lineas = {
        'Electrónicos': ['Celulares', 'Laptops', 'Tablets', 'Accesorios'],
        'Ropa': ['Camisas', 'Pantalones', 'Zapatos', 'Accesorios'],
        'Hogar': ['Cocina', 'Baño', 'Dormitorio', 'Decoración'],
        'Deportes': ['Fútbol', 'Basket', 'Running', 'Gym'],
        'Libros': ['Ficción', 'No Ficción', 'Educativos', 'Infantiles']
    }
    
    for grupo_nombre, lineas in grupos_lineas.items():
        grupo, created = GrupoArticulo.objects.get_or_create(
            nombre_grupo=grupo_nombre,
            defaults={'estado': 1}
        )
        if created:
            print(f"✅ Grupo creado: {grupo_nombre}")
        
        for linea_nombre in lineas:
            linea, created = LineaArticulo.objects.get_or_create(
                nombre_linea=linea_nombre,
                grupo=grupo,
                defaults={'estado': 1}
            )
            if created:
                print(f"  ✅ Línea creada: {linea_nombre}")
    
    print("\n🎉 ¡Datos iniciales creados exitosamente!")
    print("\n📋 Credenciales de acceso:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("   URL: http://127.0.0.1:8000/")
    print("\n🔧 Para iniciar el servidor:")
    print("   python manage.py runserver")

if __name__ == '__main__':
    try:
        create_initial_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)