# fix_migrations.py
# Script para solucionar problemas de migraciones después del reseteo

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def marcar_migraciones_basicas_como_aplicadas():
    """Marca las migraciones básicas de Django como aplicadas sin ejecutarlas"""
    print("=== MARCANDO MIGRACIONES BÁSICAS COMO APLICADAS ===")
    
    try:
        with connection.cursor() as cursor:
            # Migraciones básicas que debemos marcar como aplicadas
            migraciones_basicas = [
                ('contenttypes', '0001_initial'),
                ('auth', '0001_initial'),
                ('auth', '0002_alter_permission_name_max_length'),
                ('auth', '0003_alter_user_email_max_length'),
                ('auth', '0004_alter_user_username_opts'),
                ('auth', '0005_alter_user_last_login_null'),
                ('auth', '0006_require_contenttypes_0002'),
                ('auth', '0007_alter_validators_add_error_messages'),
                ('auth', '0008_alter_user_username_max_length'),
                ('auth', '0009_alter_user_last_name_max_length'),
                ('auth', '0010_alter_group_name_max_length'),
                ('auth', '0011_update_proxy_permissions'),
                ('auth', '0012_alter_user_first_name_max_length'),
                ('contenttypes', '0002_remove_content_type_name'),
                ('sessions', '0001_initial'),
                ('admin', '0001_initial'),
                ('admin', '0002_logentry_remove_auto_add'),
                ('admin', '0003_logentry_add_action_flag_choices'),
            ]
            
            print("Insertando registros de migraciones básicas...")
            for app, migration in migraciones_basicas:
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW()) ON CONFLICT DO NOTHING",
                    [app, migration]
                )
            
            # Verificar qué se insertó
            cursor.execute("SELECT app, COUNT(*) FROM django_migrations GROUP BY app ORDER BY app")
            result = cursor.fetchall()
            
            print("Estado después de marcar migraciones básicas:")
            for app, count in result:
                print(f"  ✓ {app}: {count} migraciones")
            
            return True
            
    except Exception as e:
        print(f"❌ Error marcando migraciones básicas: {e}")
        return False

def limpiar_datos_invalidos():
    """Eliminar datos con UUIDs inválidos"""
    print("\n=== LIMPIANDO DATOS INVÁLIDOS ===")
    
    try:
        with connection.cursor() as cursor:
            # Verificar si existen tablas de nuestro proyecto
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('articulos', 'clientes', 'usuarios')
            """)
            
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            if existing_tables:
                print("Encontradas tablas del proyecto, limpiando datos inválidos...")
                
                # Limpiar artículos con UUID inválido
                if 'articulos' in existing_tables:
                    cursor.execute("DELETE FROM articulos WHERE articulo_id = '1' OR articulo_id = '0'")
                    deleted = cursor.rowcount
                    if deleted > 0:
                        print(f"  ✓ Eliminados {deleted} artículos con UUID inválido")
                
                # Limpiar clientes con UUID inválido
                if 'clientes' in existing_tables:
                    cursor.execute("DELETE FROM clientes WHERE cliente_id = '1' OR cliente_id = '0'")
                    deleted = cursor.rowcount
                    if deleted > 0:
                        print(f"  ✓ Eliminados {deleted} clientes con UUID inválido")
                
                # Limpiar usuarios con UUID inválido
                if 'usuarios' in existing_tables:
                    cursor.execute("DELETE FROM usuarios WHERE usuario_id = '1' OR usuario_id = '0'")
                    deleted = cursor.rowcount
                    if deleted > 0:
                        print(f"  ✓ Eliminados {deleted} usuarios con UUID inválido")
            else:
                print("No se encontraron tablas del proyecto que limpiar.")
            
            return True
            
    except Exception as e:
        print(f"❌ Error limpiando datos inválidos: {e}")
        return False

def verificar_estado_final():
    """Verificar el estado final de la base de datos"""
    print("\n=== VERIFICACIÓN FINAL ===")
    
    try:
        with connection.cursor() as cursor:
            # Verificar migraciones
            cursor.execute("SELECT app, COUNT(*) FROM django_migrations GROUP BY app ORDER BY app")
            migrations = cursor.fetchall()
            
            print("Migraciones registradas:")
            for app, count in migrations:
                print(f"  ✓ {app}: {count}")
            
            # Verificar tablas existentes
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            
            tables = [row[0] for row in cursor.fetchall()]
            print(f"\nTablas existentes: {len(tables)}")
            
            basic_tables = [t for t in tables if t.startswith(('django_', 'auth_'))]
            project_tables = [t for t in tables if not t.startswith(('django_', 'auth_'))]
            
            print(f"  - Tablas básicas de Django: {len(basic_tables)}")
            print(f"  - Tablas del proyecto: {len(project_tables)}")
            
            return len(migrations) >= 3  # Al menos contenttypes, auth, sessions
            
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def main():
    print("SOLUCIONADOR DE PROBLEMAS DE MIGRACIONES\n")
    print("Este script solucionará el problema de migraciones después del reseteo.")
    print("="*70)
    
    # Paso 1: Marcar migraciones básicas como aplicadas
    if not marcar_migraciones_basicas_como_aplicadas():
        print("\n❌ Error al marcar migraciones básicas")
        return
    
    # Paso 2: Limpiar datos inválidos
    if not limpiar_datos_invalidos():
        print("\n❌ Error al limpiar datos inválidos")
        return
    
    # Paso 3: Verificar estado
    if verificar_estado_final():
        print("\n" + "="*70)
        print("✅ PROBLEMA SOLUCIONADO")
        print("\nAhora puedes ejecutar los siguientes comandos:")
        print("1. python manage.py makemigrations core")
        print("2. python manage.py migrate core")
        print("3. python manage.py createsuperuser")
        print("4. python manage.py runserver")
        print("="*70)
    else:
        print("\n❌ Aún hay problemas. Revisa los errores anteriores.")

if __name__ == '__main__':
    main()