#!/usr/bin/env python
"""
Script de instalación rápida para el Sistema POS
Ejecutar: python setup.py
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

def check_python_version():
    """Verificar la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def create_directories():
    """Crear directorios necesarios"""
    directories = [
        'static/img',
        'static/vendor', 
        'media/articulos',
        'media/profiles',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directorio creado: {directory}")

def setup_project():
    """Configurar el proyecto completo"""
    
    print("🚀 Iniciando configuración del Sistema POS...")
    print("=" * 50)
    
    # 1. Verificar Python
    if not check_python_version():
        return False
    
    # 2. Crear directorios
    print("\n📁 Creando estructura de directorios...")
    create_directories()
    
    # 3. Crear entorno virtual
    print("\n🐍 Configurando entorno virtual...")
    if platform.system() == "Windows":
        venv_command = "python -m venv venv"
        activate_command = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
        python_command = "venv\\Scripts\\python"
    else:
        venv_command = "python3 -m venv venv"
        activate_command = "source venv/bin/activate"
        pip_command = "venv/bin/pip"
        python_command = "venv/bin/python"
    
    if not run_command(venv_command, "Creando entorno virtual"):
        return False
    
    # 4. Instalar dependencias
    print("\n📦 Instalando dependencias...")
    if not run_command(f"{pip_command} install --upgrade pip", "Actualizando pip"):
        return False
    
    if not run_command(f"{pip_command} install -r requirements.txt", "Instalando dependencias"):
        return False
    
    # 5. Configurar archivo .env
    print("\n⚙️  Configurando variables de entorno...")
    if not os.path.exists('.env'):
        try:
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✅ Archivo .env creado desde .env.example")
        except FileNotFoundError:
            print("⚠️  No se encontró .env.example, creando .env básico...")
            with open('.env', 'w') as f:
                f.write("SECRET_KEY=django-insecure-change-this-in-production\n")
                f.write("DEBUG=True\n")
                f.write("DB_NAME=dbpedidos_silva\n")
                f.write("DB_USER=admin_silva\n")
                f.write("DB_PASSWORD=71749437\n")
                f.write("DB_HOST=127.0.0.1\n")
                f.write("DB_PORT=5432\n")
    else:
        print("✅ Archivo .env ya existe")
    
    # 6. Ejecutar migraciones
    print("\n🗄️  Configurando base de datos...")
    if not run_command(f"{python_command} manage.py migrate", "Aplicando migraciones de Django"):
        return False
    
    if not run_command(f"{python_command} manage.py makemigrations core", "Creando migraciones de core"):
        return False
        
    if not run_command(f"{python_command} manage.py migrate core", "Aplicando migraciones de core"):
        return False
    
    # 7. Crear datos iniciales
    print("\n👤 Creando datos iniciales...")
    if not run_command(f"{python_command} create_initial_user.py", "Creando usuario y datos iniciales"):
        return False
    
    # 8. Recopilar archivos estáticos
    print("\n📄 Recopilando archivos estáticos...")
    if not run_command(f"{python_command} manage.py collectstatic --noinput", "Recopilando archivos estáticos"):
        print("⚠️  No se pudieron recopilar archivos estáticos (normal en desarrollo)")
    
    print("\n" + "=" * 50)
    print("🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Para iniciar el servidor:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("   python manage.py runserver")
    else:
        print("   source venv/bin/activate")
        print("   python manage.py runserver")
    
    print("\n🌐 Luego visita: http://127.0.0.1:8000/")
    print("👤 Credenciales: admin / admin123")
    
    return True

if __name__ == '__main__':
    try:
        if setup_project():
            print("\n✅ ¡Todo listo para usar el Sistema POS!")
        else:
            print("\n❌ Hubo errores durante la configuración")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)