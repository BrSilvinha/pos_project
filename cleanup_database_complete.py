# cleanup_database_complete.py
# OPCIÓN ALTERNATIVA: Limpieza completa de la base de datos
# ⚠️ USAR SOLO SI EL PRIMER SCRIPT NO FUNCIONA

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
django.setup()

from django.db import connection

def eliminar_todas_las_tablas():
    """Elimina TODAS las tablas de la base de datos"""
    print("⚠️  ELIMINANDO TODAS LAS TABLAS DE LA BASE DE DATOS")
    print("⚠️  ESTO BORRARÁ TODOS LOS DATOS")
    
    try:
        with connection.cursor() as cursor:
            # Obtener todas las tablas
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            tables = [row[0] for row in cursor.fetchall()]
            
            if not tables:
                print("No hay tablas para eliminar.")
                return True
            
            print(f"Eliminando {len(tables)} tablas...")
            
            # Desactivar restricciones de clave foránea temporalmente
            cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
            
            # Eliminar todas las tablas
            for table in tables:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                    print(f"  ✓ Eliminada tabla: {table}")
                except Exception as e:
                    print(f"  ⚠️  Error eliminando {table}: {e}")
            
            # Verificar que se eliminaron todas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            remaining = cursor.fetchone()[0]
            
            if remaining == 0:
                print("✅ Todas las tablas eliminadas correctamente")
                return True
            else:
                print(f"⚠️  Aún quedan {remaining} tablas")
                return False
                
    except Exception as e:
        print(f"❌ Error eliminando tablas: {e}")
        return False

def verificar_limpieza():
    """Verificar que la base de datos está completamente limpia"""
    print("\n=== VERIFICANDO LIMPIEZA ===")
    
    try:
        with connection.cursor() as cursor:
            # Verificar tablas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            table_count = cursor.fetchone()[0]
            
            if table_count == 0:
                print("✅ Base de datos completamente limpia")
                return True
            else:
                print(f"⚠️  Aún hay {table_count} tablas")
                
                # Mostrar qué tablas quedan
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                
                remaining_tables = [row[0] for row in cursor.fetchall()]
                print("Tablas restantes:")
                for table in remaining_tables:
                    print(f"  - {table}")
                
                return False
                
    except Exception as e:
        print(f"❌ Error verificando limpieza: {e}")
        return False

def main():
    print("LIMPIEZA COMPLETA DE LA BASE DE DATOS")
    print("="*50)
    print("⚠️  ADVERTENCIA: ESTO ELIMINARÁ TODOS LOS DATOS")
    print("⚠️  USAR SOLO SI EL SCRIPT fix_migrations.py NO FUNCIONÓ")
    print("="*50)
    
    respuesta = input("¿Estás seguro de que quieres continuar? (escriba 'SI ESTOY SEGURO'): ")
    
    if respuesta != "SI ESTOY SEGURO":
        print("Operación cancelada.")
        return
    
    # Eliminar todas las tablas
    if not eliminar_todas_las_tablas():
        print("\n❌ Error durante la eliminación")
        return
    
    # Verificar limpieza
    if verificar_limpieza():
        print("\n" + "="*50)
        print("✅ BASE DE DATOS COMPLETAMENTE LIMPIA")
        print("\nAhora ejecuta estos comandos EN ORDEN:")
        print("1. python manage.py migrate")
        print("2. python manage.py makemigrations core")
        print("3. python manage.py migrate core")
        print("4. python manage.py createsuperuser")
        print("5. python manage.py runserver")
        print("="*50)
    else:
        print("\n❌ La limpieza no se completó correctamente")

if __name__ == '__main__':
    main()