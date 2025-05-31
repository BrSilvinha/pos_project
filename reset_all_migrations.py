# reset_all_migrations.py
# Reseteo completo de todas las migraciones

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.db import connection

def reset_all_migrations():
    """Resetear completamente todas las migraciones"""
    print("=== RESETEO COMPLETO DE MIGRACIONES ===")
    
    try:
        with connection.cursor() as cursor:
            # Ver estado actual
            cursor.execute("SELECT app, COUNT(*) FROM django_migrations GROUP BY app ORDER BY app;")
            current_state = cursor.fetchall()
            
            print("Estado actual de migraciones:")
            for app, count in current_state:
                print(f"  {app}: {count} migraciones")
            
            print("\nEliminando TODAS las migraciones...")
            
            # Eliminar todas las migraciones
            cursor.execute("DELETE FROM django_migrations;")
            total_deleted = cursor.rowcount
            
            print(f"✅ {total_deleted} migraciones eliminadas")
            
            # Verificar que esté limpio
            cursor.execute("SELECT COUNT(*) FROM django_migrations;")
            remaining = cursor.fetchone()[0]
            
            if remaining == 0:
                print("✅ Tabla django_migrations completamente limpia")
                return True
            else:
                print(f"⚠️  Aún quedan {remaining} migraciones")
                return False
                
    except Exception as e:
        print(f"❌ Error reseteando migraciones: {e}")
        return False

def verify_tables_state():
    """Verificar el estado de las tablas"""
    print("\n=== VERIFICANDO ESTADO DE TABLAS ===")
    
    try:
        with connection.cursor() as cursor:
            # Tablas básicas de Django que deben existir
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN (
                    'django_migrations', 'django_content_type', 'django_session',
                    'auth_permission', 'auth_group', 'auth_user', 'django_admin_log'
                )
                ORDER BY table_name;
            """)
            
            basic_tables = [row[0] for row in cursor.fetchall()]
            print(f"Tablas básicas existentes: {len(basic_tables)}")
            for table in basic_tables:
                print(f"  ✓ {table}")
            
            # Tablas de nuestro proyecto (no deberían existir)
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name NOT LIKE 'django_%'
                AND table_name NOT LIKE 'auth_%'
                ORDER BY table_name;
            """)
            
            project_tables = [row[0] for row in cursor.fetchall()]
            print(f"\nTablas del proyecto: {len(project_tables)}")
            if project_tables:
                for table in project_tables:
                    print(f"  ⚠️  {table}")
            else:
                print("  ✅ Ninguna (correcto)")
            
            return len(basic_tables) >= 5 and len(project_tables) == 0
            
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def main():
    print("RESETEO COMPLETO DEL SISTEMA DE MIGRACIONES\n")
    print("⚠️  ESTO ELIMINARÁ TODOS LOS REGISTROS DE MIGRACIONES")
    print("⚠️  DESPUÉS PODREMOS RECREAR TODO DESDE CERO")
    
    # Resetear migraciones
    if not reset_all_migrations():
        print("❌ Error en el reseteo")
        return
    
    # Verificar estado
    if verify_tables_state():
        print("\n" + "="*60)
        print("✅ RESETEO COMPLETO EXITOSO")
        print("\nAhora ejecuta estos comandos EN ORDEN:")
        print("1. python manage.py migrate")
        print("2. python manage.py makemigrations core")
        print("3. python manage.py migrate core")
        print("4. python check_real_names.py")
        print("5. python manage.py createsuperuser")
        print("6. python manage.py runserver")
        print("="*60)
    else:
        print("\n❌ El reseteo no se completó correctamente")

if __name__ == '__main__':
    main()