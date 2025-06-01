#!/usr/bin/env python
"""
Script de solución rápida para el Sistema POS
Ejecutar: python fix_installation.py
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def fix_common_issues():
    """Solucionar problemas comunes"""
    
    print("🛠️  SISTEMA POS - SOLUCIONADOR DE PROBLEMAS")
    print("=" * 50)
    
    # 1. Verificar si estamos en un entorno virtual
    if sys.prefix == sys.base_prefix:
        print("⚠️  NO estás en un entorno virtual.")
        print("   Recomendamos usar un entorno virtual:")
        if platform.system() == "Windows":
            print("   python -m venv venv")
            print("   venv\\Scripts\\activate")
        else:
            print("   python3 -m venv venv")
            print("   source venv/bin/activate")
        print()
    else:
        print("✅ Entorno virtual detectado")
    
    # 2. Actualizar pip
    print("\n📦 Actualizando pip...")
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Actualizando pip"):
        print("⚠️  No se pudo actualizar pip, continuando...")
    
    # 3. Instalar dependencias básicas
    print("\n📦 Instalando dependencias básicas...")
    basic_deps = [
        "Django==5.2.1",
        "python-decouple==3.8"
    ]
    
    for dep in basic_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️  No se pudo instalar {dep}")
    
    # 4. Instalar todas las dependencias si existe requirements.txt
    if os.path.exists('requirements.txt'):
        print("\n📦 Instalando todas las dependencias...")
        run_command(f"{sys.executable} -m pip install -r requirements.txt", "Instalando requirements.txt")
    
    # 5. Crear archivo .env si no existe
    if not os.path.exists('.env'):
        print("\n⚙️  Creando archivo .env...")
        env_content = """# Configuración del Sistema POS
SECRET_KEY=django-insecure-+a)pl$48yxx9mv+zshvj7!)q76=jmtes62&y@o5lpvrz*z$sdx
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos - cambiar a sqlite si hay problemas con PostgreSQL
DB_ENGINE=sqlite
DB_NAME=dbpedidos_silva
DB_USER=admin_silva
DB_PASSWORD=71749437
DB_HOST=127.0.0.1
DB_PORT=5432

# Email (opcional)
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password
DEFAULT_FROM_EMAIL=Sistema POS <tu_email@gmail.com>
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
    
    # 6. Ejecutar migraciones
    print("\n🗄️  Configurando base de datos...")
    
    # Primero las migraciones básicas de Django
    run_command(f"{sys.executable} manage.py migrate", "Migraciones básicas de Django")
    
    # Luego las migraciones de la app core
    run_command(f"{sys.executable} manage.py makemigrations core", "Creando migraciones de core")
    run_command(f"{sys.executable} manage.py migrate core", "Aplicando migraciones de core")
    
    # 7. Crear datos iniciales
    print("\n👤 Creando datos iniciales...")
    if os.path.exists('create_initial_user.py'):
        run_command(f"{sys.executable} create_initial_user.py", "Creando datos iniciales")
    else:
        print("⚠️  No se encontró create_initial_user.py")
    
    # 8. Verificar instalación
    print("\n🔍 Verificando instalación...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
        import django
        django.setup()
        print("✅ Django configurado correctamente")
        
        from core.models import Usuario
        admin_count = Usuario.objects.filter(is_superuser=True).count()
        print(f"✅ Usuarios administrador: {admin_count}")
        
    except Exception as e:
        print(f"⚠️  Error en verificación: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 PROCESO COMPLETADO")
    print("\n📋 Para iniciar el servidor:")
    print("   python manage.py runserver")
    print("\n🌐 Luego visita: http://127.0.0.1:8000/")
    print("👤 Credenciales: admin / admin123")
    
    print("\n🔧 Si sigues teniendo problemas:")
    print("   1. Verifica que estés en un entorno virtual")
    print("   2. Instala manualmente: pip install python-decouple")
    print("   3. Cambia DB_ENGINE=sqlite en el archivo .env")

if __name__ == '__main__':
    try:
        fix_common_issues()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")