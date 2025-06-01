#!/usr/bin/env python
"""
Script CORREGIDO para arreglar referencias de namespace 'core:' en templates
Ejecutar: python fix_namespace_corrected.py
"""

import os
import glob

def fix_namespace_in_templates():
    """Corregir referencias de namespace en todos los templates"""
    
    print("🔧 INICIANDO CORRECCIÓN DE NAMESPACE")
    print("=" * 50)
    
    # Mapeo simple de texto a reemplazar
    replacements = [
        ("{% url 'core:articulos_list' %}", "{% url 'articulos_list' %}"),
        ("{% url 'core:articulo_create' %}", "{% url 'articulo_create' %}"),
        ("{% url 'core:articulo_detail'", "{% url 'articulo_detail'"),
        ("{% url 'core:articulo_edit'", "{% url 'articulo_edit'"),
        ("{% url 'core:articulo_delete'", "{% url 'articulo_delete'"),
        ("{% url 'core:cart_detail' %}", "{% url 'cart_detail' %}"),
        ("{% url 'core:cart_add'", "{% url 'cart_add'"),
        ("{% url 'core:cart_remove'", "{% url 'cart_remove'"),
        ("{% url 'core:cart_clear' %}", "{% url 'cart_clear' %}"),
        ("{% url 'core:checkout' %}", "{% url 'checkout' %}"),
        ("{% url 'core:order_list' %}", "{% url 'order_list' %}"),
        ("{% url 'core:order_detail'", "{% url 'order_detail'"),
        ("{% url 'core:dashboard' %}", "{% url 'dashboard' %}"),
        ("{% url 'core:home' %}", "{% url 'home' %}"),
        ("{% url 'core:profile' %}", "{% url 'profile' %}"),
        ("{% url 'core:login' %}", "{% url 'login' %}"),
        ("{% url 'core:logout' %}", "{% url 'logout' %}"),
    ]
    
    # Buscar todos los archivos .html
    template_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
    
    if not template_files:
        print("❌ No se encontraron archivos HTML")
        return False
    
    archivos_corregidos = 0
    total_cambios = 0
    
    for template_file in template_files:
        print(f"\n📄 Procesando: {template_file}")
        
        try:
            # Leer el archivo
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            cambios_archivo = 0
            
            # Aplicar reemplazos
            for old_text, new_text in replacements:
                if old_text in content:
                    count = content.count(old_text)
                    content = content.replace(old_text, new_text)
                    cambios_archivo += count
                    if count > 0:
                        print(f"  ✅ '{old_text}' → '{new_text}' ({count}x)")
            
            # Guardar si hubo cambios
            if content != original_content:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                archivos_corregidos += 1
                total_cambios += cambios_archivo
                print(f"  💾 Guardado con {cambios_archivo} cambios")
            else:
                print(f"  ✅ Sin cambios necesarios")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print(f"🎉 CORRECCIÓN COMPLETADA")
    print(f"📁 Archivos procesados: {len(template_files)}")
    print(f"📝 Archivos corregidos: {archivos_corregidos}")
    print(f"🔄 Total cambios: {total_cambios}")
    
    return archivos_corregidos > 0

def create_fixed_template():
    """Crear template correcto para crear artículos"""
    
    template_dir = "templates/articulos"
    template_file = os.path.join(template_dir, "crear.html")
    
    # Crear directorio
    os.makedirs(template_dir, exist_ok=True)
    
    template_content = """{% extends 'base.html' %}
{% load static %}

{% block title %}
    {% if edit_mode %}Editar{% else %}Crear{% endif %} Artículo - Sistema POS
{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="h3">
        <i class="fas fa-{% if edit_mode %}edit{% else %}plus{% endif %} me-2"></i>
        {% if edit_mode %}Editar{% else %}Crear{% endif %} Artículo
    </h2>
    <a href="{% url 'articulos_list' %}" class="btn btn-outline-secondary">
        <i class="fas fa-arrow-left me-1"></i>Volver
    </a>
</div>

<div class="row">
    <div class="col-lg-8">
        <div class="card shadow">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Información del Artículo</h6>
            </div>
            <div class="card-body">
                <form method="post" id="articleForm">
                    {% csrf_token %}
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="codigo_articulo" class="form-label">
                                Código del Artículo <span class="text-danger">*</span>
                            </label>
                            <input type="text" class="form-control" id="codigo_articulo" name="codigo_articulo" 
                                   required maxlength="50" placeholder="Ej: ART-001">
                        </div>
                        <div class="col-md-6">
                            <label for="codigo_barras" class="form-label">Código de Barras</label>
                            <input type="text" class="form-control" id="codigo_barras" name="codigo_barras" 
                                   maxlength="100" placeholder="Opcional">
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="descripcion" class="form-label">
                            Descripción <span class="text-danger">*</span>
                        </label>
                        <input type="text" class="form-control" id="descripcion" name="descripcion" 
                               required maxlength="255" placeholder="Descripción del producto">
                    </div>

                    <div class="mb-3">
                        <label for="presentacion" class="form-label">Presentación</label>
                        <input type="text" class="form-control" id="presentacion" name="presentacion" 
                               maxlength="100" placeholder="Ej: Unidad, Caja">
                    </div>

                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="grupo" class="form-label">
                                Grupo <span class="text-danger">*</span>
                            </label>
                            <select class="form-select" id="grupo" name="grupo" required>
                                <option value="">-- Seleccionar Grupo --</option>
                                {% for grupo in grupos %}
                                <option value="{{ grupo.grupo_id }}">{{ grupo.nombre_grupo }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label for="linea" class="form-label">
                                Línea <span class="text-danger">*</span>
                            </label>
                            <select class="form-select" id="linea" name="linea" required>
                                <option value="">-- Seleccionar Línea --</option>
                            </select>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="stock" class="form-label">Stock Inicial</label>
                        <input type="number" class="form-control" id="stock" name="stock" 
                               min="0" value="0">
                    </div>
                </form>
            </div>
        </div>
    </div>

    <div class="col-lg-4">
        <div class="card shadow">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Precios</h6>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label for="precio_1" class="form-label">
                        Precio de Venta <span class="text-danger">*</span>
                    </label>
                    <input type="number" class="form-control" id="precio_1" name="precio_1" 
                           step="0.01" min="0" required placeholder="0.00">
                </div>

                <div class="mb-3">
                    <label for="precio_2" class="form-label">Precio 2</label>
                    <input type="number" class="form-control" id="precio_2" name="precio_2" 
                           step="0.01" min="0" placeholder="0.00">
                </div>

                <div class="d-grid gap-2">
                    <button type="submit" form="articleForm" class="btn btn-primary">
                        <i class="fas fa-save me-1"></i>Crear Artículo
                    </button>
                    
                    <a href="{% url 'articulos_list' %}" class="btn btn-outline-secondary">
                        <i class="fas fa-times me-1"></i>Cancelar
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const grupoSelect = document.getElementById('grupo');
    const lineaSelect = document.getElementById('linea');
    
    if (grupoSelect && lineaSelect) {
        grupoSelect.addEventListener('change', function() {
            const grupoId = this.value;
            lineaSelect.innerHTML = '<option value="">-- Seleccionar Línea --</option>';
            
            if (grupoId) {
                fetch('/api/lineas-por-grupo/' + grupoId + '/')
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(linea => {
                            const option = document.createElement('option');
                            option.value = linea.id;
                            option.textContent = linea.nombre;
                            lineaSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    }
});
</script>
{% endblock %}"""
    
    try:
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        print(f"✅ Template creado: {template_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando template: {e}")
        return False

def main():
    """Función principal"""
    
    print("🛠️  CORRECTOR DE NAMESPACE - VERSIÓN CORREGIDA")
    print("=" * 60)
    
    # 1. Crear template correcto
    print("\n1️⃣ Creando template correcto...")
    create_fixed_template()
    
    # 2. Corregir otros templates
    print("\n2️⃣ Corrigiendo referencias en templates...")
    success = fix_namespace_in_templates()
    
    print("\n" + "=" * 60)
    print("🎉 PROCESO COMPLETADO")
    print("\n📋 AHORA EJECUTA:")
    print("   python manage.py runserver")
    print("   Ve a: http://127.0.0.1:8000/articulos/crear/")
    
    return True

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")