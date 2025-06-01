#!/usr/bin/env python
"""
Script para solucionar el error de WeasyPrint en Windows
Ejecutar: python fix_weasyprint_error.py
"""

import os
import sys

def fix_weasyprint_import():
    """
    Soluciona el problema de importación de WeasyPrint
    """
    print("🛠️  SOLUCIONANDO PROBLEMA DE WEASYPRINT")
    print("=" * 50)
    
    views_file = "core/views.py"
    
    if not os.path.exists(views_file):
        print("❌ No se encontró core/views.py")
        return False
    
    # Leer el archivo actual
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya está corregido
    if "except (ImportError, OSError)" in content:
        print("✅ Ya está corregido")
        return True
    
    # Buscar y reemplazar la importación problemática
    old_import = """# Para WeasyPrint
try:
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False"""
    
    new_import = """# Para WeasyPrint - Opcional (puede fallar en Windows)
try:
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
    print("✅ WeasyPrint disponible")
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"⚠️  WeasyPrint no disponible: {e}")
    print("📄 Usando solo ReportLab para generar PDFs")"""
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        
        # Guardar el archivo corregido
        with open(views_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Archivo core/views.py corregido")
        return True
    else:
        print("⚠️  No se encontró el código a reemplazar")
        return False

def test_django():
    """
    Probar que Django funciona después de la corrección
    """
    print("\n🧪 Probando Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_project.settings')
        import django
        django.setup()
        print("✅ Django configurado correctamente")
        
        from core.models import Usuario
        print("✅ Modelos importados correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🚀 INICIANDO SOLUCIÓN...")
    
    # 1. Corregir importación de WeasyPrint
    if fix_weasyprint_import():
        print("✅ Importación corregida")
    else:
        print("⚠️  No se pudo corregir automáticamente")
    
    # 2. Probar Django
    if test_django():
        print("✅ Django funciona correctamente")
    else:
        print("❌ Aún hay problemas con Django")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡PROBLEMA SOLUCIONADO!")
    print("\n📋 Ahora puedes ejecutar:")
    print("   python manage.py runserver")
    print("\n🌐 Y visitar: http://127.0.0.1:8000/")
    print("\n📄 NOTA: WeasyPrint está deshabilitado.")
    print("   Usa ReportLab para generar PDFs (funciona perfectamente)")
    
    return True

if __name__ == '__main__':
    try:
        if main():
            print("\n✅ ¡Listo para usar!")
        else:
            print("\n❌ Revisa los errores arriba")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")