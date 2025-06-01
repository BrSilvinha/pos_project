# 🛒 Sistema POS (Point of Sale)

Un sistema completo de punto de venta desarrollado con Django 5.2, diseñado para gestionar inventarios, ventas y clientes de manera eficiente y moderna.

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías-utilizadas)
- [Requisitos](#-requisitos-del-sistema)
- [Instalación Rápida](#-instalación-rápida)
- [Instalación Manual](#-instalación-manual)
- [Configuración](#-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## 🚀 Características

### 📦 Gestión de Inventario
- ✅ **Administración de Artículos**: Crear, editar, eliminar y consultar productos
- ✅ **Organización por Grupos y Líneas**: Categorización jerárquica de productos
- ✅ **Control de Stock**: Monitoreo en tiempo real con alertas de stock bajo
- ✅ **Códigos de Barras**: Soporte para códigos de producto únicos
- ✅ **Gestión de Precios**: Múltiples precios por producto (venta, compra, costo)

### 🛍️ Sistema de Ventas
- ✅ **Carrito de Compras**: Interfaz intuitiva para agregar productos
- ✅ **Gestión de Órdenes**: Crear, procesar y seguir órdenes de compra
- ✅ **Clientes y Vendedores**: Administración completa de usuarios de negocio
- ✅ **Histórico de Transacciones**: Seguimiento completo de ventas
- ✅ **Generación de PDF**: Facturas y órdenes en formato PDF

### 👥 Gestión de Usuarios
- ✅ **Sistema de Autenticación**: Login/logout seguro con sesiones
- ✅ **Roles de Usuario**: Administradores, staff y usuarios regulares
- ✅ **Perfiles Personalizados**: Información detallada de usuarios
- ✅ **Control de Acceso**: Permisos basados en roles

### 🎨 Interfaz de Usuario
- ✅ **Diseño Responsive**: Optimizado para desktop, tablet y móvil
- ✅ **Dashboard Interactivo**: Estadísticas y métricas en tiempo real
- ✅ **Búsqueda Avanzada**: Filtros y búsqueda rápida de productos
- ✅ **Navegación Intuitiva**: UX moderna con Bootstrap 5
- ✅ **Temas Modernos**: Gradientes y efectos visuales atractivos

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.12**: Lenguaje de programación principal
- **Django 5.2**: Framework web robusto y escalable
- **PostgreSQL**: Base de datos relacional de alto rendimiento
- **UUID**: Identificadores únicos para seguridad
- **ReportLab**: Generación de PDFs

### Frontend
- **Bootstrap 5.3**: Framework CSS para diseño responsive
- **Font Awesome 6**: Iconografía moderna y profesional
- **JavaScript ES6**: Interactividad y funcionalidades dinámicas
- **HTML5 & CSS3**: Estructura y estilos modernos
- **Gradientes CSS**: Diseño visual atractivo

### Herramientas de Desarrollo
- **Git**: Control de versiones
- **Django Admin**: Panel de administración integrado
- **Psycopg2**: Adaptador PostgreSQL para Python
- **Python Decouple**: Gestión de variables de entorno

## 📋 Requisitos del Sistema

### Software Requerido
- **Python**: 3.12 o superior
- **PostgreSQL**: 15 o superior (opcional, puede usar SQLite)
- **Git**: Para clonar el repositorio

### Dependencias Python
Las dependencias se instalan automáticamente desde `requirements.txt`:
```txt
Django==5.2.1
psycopg2-binary==2.9.7
Pillow==10.0.0
python-decouple==3.8
reportlab==4.0.4
```

## 🚀 Instalación Rápida

### Opción 1: Script de Instalación Automática
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/sistema-pos.git
cd sistema-pos

# Ejecutar instalación automática
python setup.py

# Iniciar el servidor
python manage.py runserver
```

### Opción 2: Una Línea (Windows)
```cmd
git clone https://github.com/tu-usuario/sistema-pos.git && cd sistema-pos && python setup.py
```

### Opción 3: Una Línea (Linux/macOS)
```bash
git clone https://github.com/tu-usuario/sistema-pos.git && cd sistema-pos && python3 setup.py
```

## 🔧 Instalación Manual

Si prefieres instalar paso a paso:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sistema-pos.git
cd sistema-pos
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### Para SQLite (Desarrollo - Más Simple)
```bash
# No necesita configuración adicional
python manage.py migrate
```

#### Para PostgreSQL (Producción)
```sql
-- En PostgreSQL, crear:
CREATE DATABASE dbpedidos_silva;
CREATE USER admin_silva WITH PASSWORD '71749437';
GRANT ALL PRIVILEGES ON DATABASE dbpedidos_silva TO admin_silva;
```

Luego crear archivo `.env`:
```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura
DEBUG=True
DB_ENGINE=postgresql
DB_NAME=dbpedidos_silva
DB_USER=admin_silva
DB_PASSWORD=71749437
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Ejecutar Migraciones
```bash
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
```

### 6. Crear Datos Iniciales
```bash
python create_initial_user.py
```

### 7. Iniciar Servidor
```bash
python manage.py runserver
```

## ⚙️ Configuración

### Variables de Entorno (.env)
```env
# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Base de Datos
DB_ENGINE=sqlite  # o postgresql
DB_NAME=dbpedidos_silva
DB_USER=admin_silva
DB_PASSWORD=71749437
DB_HOST=127.0.0.1
DB_PORT=5432

# Email (Opcional)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-app
```

### Configuración de Base de Datos
El sistema soporta tanto SQLite como PostgreSQL:

- **SQLite**: Ideal para desarrollo, no requiere instalación adicional
- **PostgreSQL**: Recomendado para producción, mayor rendimiento

### Configuración de Archivos Estáticos
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

## 📖 Uso del Sistema

### Acceso Inicial
1. **URL**: http://127.0.0.1:8000/
2. **Usuario Administrador**: `admin`
3. **Contraseña**: `admin123`

### Flujo de Trabajo Típico

#### 1. Configuración Inicial
- ✅ Acceder al sistema con credenciales de administrador
- ✅ Verificar grupos y líneas de artículos en el panel de administración
- ✅ Configurar tipos de identificación y canales si es necesario

#### 2. Gestión de Productos
```
Dashboard → Artículos → Nuevo Artículo
1. Completar código único del artículo
2. Agregar descripción detallada
3. Seleccionar grupo y línea
4. Configurar stock inicial
5. Establecer precios de venta
6. Guardar artículo
```

#### 3. Proceso de Venta
```
Lista de Artículos → Seleccionar Producto → Agregar al Carrito
1. Buscar productos en el catálogo
2. Seleccionar cantidad deseada
3. Agregar al carrito de compras
4. Revisar productos en el carrito
5. Proceder al checkout
6. Completar información de entrega
7. Finalizar orden
```

#### 4. Administración Avanzada
- 📊 Monitorear estadísticas desde el dashboard
- 📦 Gestionar stock bajo con alertas automáticas
- 📋 Revisar órdenes pendientes y procesadas
- 👥 Administrar clientes y vendedores
- 📄 Generar reportes en PDF

## 📁 Estructura del Proyecto

```
pos_project/
├── 📁 core/                          # Aplicación principal
│   ├── 📁 management/commands/        # Comandos personalizados Django
│   ├── 📁 migrations/                 # Migraciones de base de datos
│   ├── 📄 admin.py                    # Configuración del panel admin
│   ├── 📄 apps.py                     # Configuración de la aplicación
│   ├── 📄 cart.py                     # Lógica del carrito de compras
│   ├── 📄 forms.py                    # Formularios de Django
│   ├── 📄 models.py                   # Modelos de datos
│   ├── 📄 urls.py                     # URLs de la aplicación
│   └── 📄 views.py                    # Vistas y lógica de negocio
├── 📁 pos_project/                    # Configuración del proyecto
│   ├── 📄 settings.py                 # Configuración principal de Django
│   ├── 📄 urls.py                     # URLs principales del proyecto
│   ├── 📄 choices.py                  # Opciones y constantes
│   └── 📄 wsgi.py                     # Configuración para despliegue
├── 📁 templates/                      # Plantillas HTML
│   ├── 📁 accounts/                   # Templates de autenticación
│   ├── 📁 core/                       # Templates principales
│   │   ├── 📁 articulos/              # Templates de productos
│   │   └── 📁 cart/                   # Templates de carrito y órdenes
│   ├── 📁 emails/                     # Templates de emails
│   ├── 📄 base.html                   # Template base del sitio
│   └── 📄 navbar.html                 # Barra de navegación
├── 📁 static/                         # Archivos estáticos
│   ├── 📁 css/                        # Estilos CSS personalizados
│   └── 📁 js/                         # JavaScript personalizado
├── 📄 manage.py                       # Script de gestión de Django
├── 📄 requirements.txt                # Dependencias del proyecto
├── 📄 create_initial_user.py          # Script de inicialización
├── 📄 setup.py                        # Script de instalación automática
├── 📄 fix_nuclear.py                  # Script de solución de problemas
└── 📄 README.md                       # Este archivo
```

## 🔌 API Endpoints

### Autenticación
- `GET/POST /login/` - Iniciar sesión
- `GET /logout/` - Cerrar sesión
- `GET /profile/` - Perfil de usuario

### Dashboard y Navegación
- `GET /` - Dashboard principal con estadísticas
- `GET /home/` - Página de inicio (alias del dashboard)

### Gestión de Artículos
- `GET /articulos/` - Lista paginada de artículos con búsqueda
- `GET /articulos/crear/` - Formulario para crear nuevo artículo
- `POST /articulos/crear/` - Procesar creación de artículo
- `GET /articulos/<uuid>/` - Detalle de artículo específico
- `GET /articulos/<uuid>/editar/` - Formulario de edición
- `POST /articulos/<uuid>/editar/` - Procesar edición
- `GET /articulos/<uuid>/eliminar/` - Confirmación de eliminación
- `POST /articulos/<uuid>/eliminar/` - Procesar eliminación

### Carrito de Compras
- `GET /carrito/` - Ver contenido del carrito
- `POST /carrito/agregar/<uuid>/` - Agregar producto al carrito
- `GET /carrito/eliminar/<uuid>/` - Eliminar producto del carrito
- `GET /carrito/vaciar/` - Vaciar todo el carrito

### Órdenes de Compra
- `GET /checkout/` - Formulario de finalización de compra
- `POST /checkout/` - Procesar orden de compra
- `GET /ordenes/` - Lista de órdenes del usuario
- `GET /orden/<uuid>/` - Detalle de orden específica
- `GET /orden/cancelar/<uuid>/` - Cancelar orden pendiente
- `GET /orden/pdf/<uuid>/` - Generar PDF de la orden

### API Interna
- `GET /api/lineas-por-grupo/<int>/` - Obtener líneas por grupo (JSON)

## 🐛 Solución de Problemas

### Error "RelatedObjectDoesNotExist"
```bash
# Ejecutar limpieza nuclear de la base de datos
python fix_nuclear.py

# O resetear migraciones manualmente
python manage.py migrate --fake core zero
python manage.py migrate core
```

### Error "NoReverseMatch" (namespace 'core')
El template debe usar URLs sin namespace:
```html
<!-- ❌ Incorrecto -->
<a href="{% url 'core:articulos_list' %}">

<!-- ✅ Correcto -->
<a href="{% url 'articulos_list' %}">
```

### Error de Migración
```bash
# Resetear todas las migraciones
rm core/migrations/0*.py
python manage.py makemigrations core
python manage.py migrate
```

### Error de Base de Datos
```bash
# Verificar conexión PostgreSQL
python manage.py dbshell

# O cambiar a SQLite para desarrollo
# En .env: DB_ENGINE=sqlite
```

### Error de Archivos Estáticos
```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### Limpiar Datos Inconsistentes
```bash
# Usar comando personalizado
python manage.py cleanup_database --fix
```

## 🎯 Características Avanzadas

### Sistema de Carrito Basado en Sesiones
- ✅ Persistencia automática en la sesión del usuario
- ✅ Cálculo dinámico de totales y subtotales
- ✅ Validación de stock en tiempo real
- ✅ Actualización de cantidades sin recargar página

### Generación de PDFs
- ✅ Facturas profesionales con ReportLab
- ✅ Diseño corporativo personalizable
- ✅ Información completa del cliente y productos
- ✅ Descarga directa desde el navegador

### Dashboard Inteligente
- ✅ Estadísticas en tiempo real
- ✅ Alertas de stock bajo
- ✅ Órdenes pendientes de procesamiento
- ✅ Accesos rápidos a funciones principales

### Búsqueda Avanzada
- ✅ Búsqueda por código, descripción y código de barras
- ✅ Filtros por stock, grupo y línea
- ✅ Paginación eficiente para grandes catálogos
- ✅ Resultados en tiempo real

## 🔒 Seguridad

### Medidas Implementadas
- ✅ **Autenticación robusta**: Sistema de login seguro con Django
- ✅ **Control de acceso**: Permisos basados en roles de usuario
- ✅ **Protección CSRF**: Tokens de seguridad en formularios
- ✅ **Validación de datos**: Sanitización de inputs del usuario
- ✅ **UUIDs**: Identificadores únicos no secuenciales
- ✅ **Sesiones seguras**: Configuración optimizada para producción

### Configuración para Producción
```python
# En settings.py para producción
DEBUG = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 📊 Rendimiento

### Optimizaciones Implementadas
- ✅ **Consultas optimizadas**: select_related y prefetch_related
- ✅ **Paginación eficiente**: Carga incremental de datos
- ✅ **Caché de sesiones**: Almacenamiento optimizado del carrito
- ✅ **Índices de base de datos**: Búsquedas rápidas por código y descripción
- ✅ **Lazy loading**: Carga bajo demanda de componentes

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos para contribuir:

### 1. Fork y Clonar
```bash
git clone https://github.com/tu-usuario/sistema-pos.git
cd sistema-pos
```

### 2. Crear Rama de Feature
```bash
git checkout -b feature/nueva-funcionalidad
```

### 3. Realizar Cambios
```bash
# Hacer cambios en el código
git add .
git commit -m "feat: agregar nueva funcionalidad increíble"
```

### 4. Ejecutar Pruebas
```bash
python manage.py test
python manage.py check
```

### 5. Push y Pull Request
```bash
git push origin feature/nueva-funcionalidad
# Crear Pull Request en GitHub
```

### Guías de Contribución
- 📝 Sigue las convenciones de código de Django y PEP 8
- 🧪 Incluye tests para nuevas funcionalidades
- 📚 Actualiza la documentación para cambios importantes
- 💬 Usa mensajes de commit descriptivos (formato Conventional Commits)
- 🔍 Verifica que no hay errores con `python manage.py check`

### Tipos de Contribuciones Buscadas
- 🐛 Corrección de bugs
- ⚡ Mejoras de rendimiento
- 🎨 Mejoras de UI/UX
- 📱 Responsive design
- 🌐 Internacionalización
- 📊 Nuevos reportes y estadísticas
- 🔒 Mejoras de seguridad
- 📚 Documentación

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 Sistema POS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📞 Contacto y Soporte

- **Desarrollador**: Tu Nombre
- **Email**: tu.email@ejemplo.com
- **LinkedIn**: [tu-perfil](https://linkedin.com/in/tu-perfil)
- **GitHub**: [tu-usuario](https://github.com/tu-usuario)
- **Issues**: [Reportar problemas](https://github.com/tu-usuario/sistema-pos/issues)

## 🙏 Agradecimientos

- **Django Community** - Por el excelente framework web
- **Bootstrap Team** - Por los componentes UI responsivos
- **PostgreSQL** - Por la base de datos robusta y confiable
- **Font Awesome** - Por los iconos profesionales
- **ReportLab** - Por la generación de PDFs
- **Python Software Foundation** - Por el lenguaje de programación

---

⭐ **¡Si este proyecto te ayudó, considera darle una estrella en GitHub!** ⭐

## 📈 Próximas Mejoras

### Versión 1.1 (Próximamente)
- [ ] 📊 Sistema de reportes avanzados con gráficos
- [ ] 💳 Integración con pasarelas de pago (PayPal, Stripe)
- [ ] 📱 PWA (Progressive Web App) para uso offline
- [ ] 🔔 Sistema de notificaciones push
- [ ] 📧 Notificaciones por email automáticas
- [ ] 🔍 Búsqueda con autocompletado y sugerencias

### Versión 1.2 (Planificado)
- [ ] 📱 Aplicación móvil nativa (React Native)
- [ ] 🏪 Módulo de múltiples tiendas
- [ ] 👥 Sistema de roles y permisos granular
- [ ] 📊 Dashboard de analytics con métricas avanzadas
- [ ] 🔗 API REST completa para integraciones
- [ ] 🌐 Soporte multiidioma (i18n)

### Versión 2.0 (Futuro)
- [ ] 🧾 Módulo de facturación electrónica
- [ ] 📈 Integración con sistemas contables
- [ ] 🎯 Sistema de marketing y promociones
- [ ] 📦 Gestión avanzada de inventarios (lotes, vencimientos)
- [ ] 🔄 Sincronización en tiempo real multi-dispositivo
- [ ] 🤖 Inteligencia artificial para predicción de ventas

## 🔄 Historial de Versiones

### v1.0.0 (Actual)
- ✅ Sistema completo de gestión de artículos
- ✅ Carrito de compras funcional
- ✅ Gestión de órdenes y clientes
- ✅ Dashboard con estadísticas
- ✅ Generación de PDFs
- ✅ Sistema de autenticación
- ✅ Panel de administración

### v0.9.0 (Beta)
- ✅ Funcionalidades básicas implementadas
- ✅ Pruebas y corrección de errores
- ✅ Documentación completa

### v0.8.0 (Alpha)
- ✅ Prototipo inicial
- ✅ Modelos de datos definidos
- ✅ Interfaz básica implementada

---

**Desarrollado con ❤️ usando Django, Bootstrap y mucho café ☕**

*Sistema POS - Transformando la gestión de ventas, un código a la vez.*
