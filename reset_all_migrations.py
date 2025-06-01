#!/usr/bin/env python
"""
Script para resetear todas las migraciones del proyecto
CUIDADO: Esto eliminará todos los datos de la base de datos
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def reset_migrations():
    """Resetear todas las migraciones"""
    
    print("⚠️  ADVERTENCIA: Este script eliminará todos los datos de la base de datos")
    respuesta = input("¿Estás seguro de continuar? (escribe 'SI' para confirmar): ")
    
    if respuesta != 'SI':
        print("❌ Operación cancelada")
        return
    
    print("🔄 Iniciando reset de migraciones...")
    
    try:
        # 1. Eliminar archivos de migración
        print("📂 Eliminando archivos de migración...")
        
        migrations_dir = Path('core/migrations')
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.py'):
                if file.name != '__init__.py':
                    file.unlink()
                    print(f"   ✅ Eliminado: {file}")
        
        # 2. Eliminar la base de datos SQLite si existe
        db_path = Path('db.sqlite3')
        if db_path.exists():
            db_path.unlink()
            print("   ✅ Base de datos SQLite eliminada")
        
        # 3. Para PostgreSQL, eliminar tablas
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            print("🗄️  Eliminando tablas de PostgreSQL...")
            
            with connection.cursor() as cursor:
                # Obtener todas las tablas
                cursor.execute("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public' 
                    AND tablename NOT LIKE 'pg_%' 
                    AND tablename != 'information_schema'
                """)
                
                tables = [row[0] for row in cursor.fetchall()]
                
                if tables:
                    # Eliminar tablas con CASCADE
                    for table in tables:
                        try:
                            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                            print(f"   ✅ Tabla eliminada: {table}")
                        except Exception as e:
                            print(f"   ⚠️  Error eliminando tabla {table}: {e}")
                    
                    # Limpiar tabla de migraciones de Django
                    cursor.execute("DROP TABLE IF EXISTS django_migrations CASCADE;")
                    print("   ✅ Tabla django_migrations eliminada")
        
        # 4. Crear nuevas migraciones
        print("📝 Creando nuevas migraciones...")
        execute_from_command_line(['manage.py', 'makemigrations', 'core'])
        
        # 5. Aplicar migraciones
        print("⚡ Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("\n🎉 ¡Reset de migraciones completado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("   1. python create_initial_user.py")
        print("   2. python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Error durante el reset: {e}")
        sys.exit(1)

if __name__ == '__main__':
    reset_migrations()