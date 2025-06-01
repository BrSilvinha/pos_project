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
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Capturas de Pantalla](#-capturas-de-pantalla)
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

### 👥 Gestión de Usuarios
- ✅ **Sistema de Autenticación**: Login/logout seguro
- ✅ **Roles de Usuario**: Administradores, staff y usuarios regulares
- ✅ **Perfiles Personalizados**: Información detallada de usuarios
- ✅ **Sesiones Seguras**: Manejo seguro de sesiones de usuario

### 🎨 Interfaz de Usuario
- ✅ **Diseño Responsive**: Optimizado para desktop, tablet y móvil
- ✅ **Dashboard Interactivo**: Estadísticas y métricas en tiempo real
- ✅ **Búsqueda Avanzada**: Filtros y búsqueda rápida de productos
- ✅ **Navegación Intuitiva**: UX moderna con Bootstrap 5

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.12**: Lenguaje de programación principal
- **Django 5.2**: Framework web robusto y escalable
- **PostgreSQL**: Base de datos relacional de alto rendimiento
- **UUID**: Identificadores únicos para seguridad

### Frontend
- **Bootstrap 5.3**: Framework CSS para diseño responsive
- **Font Awesome 6**: Iconografía moderna y profesional
- **JavaScript ES6**: Interactividad y funcionalidades dinámicas
- **HTML5 & CSS3**: Estructura y estilos modernos

### Herramientas
- **Git**: Control de versiones
- **Django Admin**: Panel de administración integrado
- **Psycopg2**: Adaptador PostgreSQL para Python

## 📋 Requisitos del Sistema

### Software Requerido
- **Python**: 3.12 o superior
- **PostgreSQL**: 15 o superior
- **Git**: Para clonar el repositorio

### Dependencias Python
```txt
Django==5.2.1
psycopg2-binary==2.9.7
Pillow==10.0.0
python-decouple==3.8
```

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sistema-pos.git
cd sistema-pos
```

### 2. Crear Entorno Virtual
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE dbpedidos_silva;
CREATE USER admin_silva WITH PASSWORD '71749437';
GRANT ALL PRIVILEGES ON DATABASE dbpedidos_silva TO admin_silva;
```

### 5. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
DB_NAME=dbpedidos_silva
DB_USER=admin_silva
DB_PASSWORD=71749437
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 6. Ejecutar Migraciones
```bash
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
```

### 7. Crear Datos Iniciales
```bash
python create_initial_user.py
```

### 8. Iniciar Servidor
```bash
python manage.py runserver
```

## ⚙️ Configuración

### Configuración de Base de Datos
El proyecto está configurado para PostgreSQL por defecto. Para cambiar a SQLite en desarrollo:

```python
# En settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Configuración de Archivos Estáticos
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

### Configuración de Media
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 📖 Uso del Sistema

### Acceso al Sistema
1. **URL**: http://127.0.0.1:8000/
2. **Usuario Administrador**: `admin`
3. **Contraseña**: `admin123`

### Flujo de Trabajo Típico

#### 1. Configuración Inicial
- Acceder al panel de administración
- Crear grupos y líneas de artículos
- Configurar tipos de identificación y canales

#### 2. Gestión de Productos
- Navegar a "Artículos" > "Lista de Artículos"
- Crear nuevos productos con códigos únicos
- Asignar precios y stock inicial
- Organizar por grupos y líneas

#### 3. Proceso de Venta
- Buscar productos en el catálogo
- Agregar productos al carrito
- Revisar y modificar cantidades
- Proceder al checkout
- Generar orden de compra

#### 4. Administración
- Monitorear stock bajo desde el dashboard
- Gestionar clientes y vendedores
- Revisar órdenes pendientes
- Generar reportes

## 📁 Estructura del Proyecto

```
pos_project/
├── 📁 core/                          # Aplicación principal
│   ├── 📁 management/commands/        # Comandos personalizados
│   ├── 📁 migrations/                 # Migraciones de base de datos
│   ├── 📄 admin.py                    # Configuración del admin
│   ├── 📄 apps.py                     # Configuración de la app
│   ├── 📄 cart.py                     # Lógica del carrito
│   ├── 📄 forms.py                    # Formularios de Django
│   ├── 📄 models.py                   # Modelos de datos
│   ├── 📄 urls.py                     # URLs de la aplicación
│   └── 📄 views.py                    # Vistas y lógica de negocio
├── 📁 pos_project/                    # Configuración del proyecto
│   ├── 📄 settings.py                 # Configuración de Django
│   ├── 📄 urls.py                     # URLs principales
│   ├── 📄 choices.py                  # Opciones de modelos
│   └── 📄 wsgi.py                     # Configuración WSGI
├── 📁 templates/                      # Plantillas HTML
│   ├── 📁 accounts/                   # Templates de autenticación
│   ├── 📁 core/                       # Templates principales
│   │   ├── 📁 articulos/              # Templates de productos
│   │   └── 📁 cart/                   # Templates de carrito
│   ├── 📄 base.html                   # Template base
│   └── 📄 navbar.html                 # Navegación
├── 📁 static/                         # Archivos estáticos
│   ├── 📁 css/                        # Estilos CSS
│   └── 📁 js/                         # JavaScript
├── 📄 manage.py                       # Script de gestión de Django
├── 📄 requirements.txt                # Dependencias del proyecto
├── 📄 create_initial_user.py          # Script de inicialización
└── 📄 README.md                       # Este archivo
```

## 🔌 API Endpoints

### Autenticación
- `GET/POST /login/` - Iniciar sesión
- `GET /logout/` - Cerrar sesión
- `GET /profile/` - Perfil de usuario

### Dashboard
- `GET /` - Dashboard principal
- `GET /home/` - Página de inicio

### Artículos
- `GET /articulos/` - Lista de artículos
- `GET /articulos/<uuid>/` - Detalle de artículo

### Carrito
- `GET /carrito/` - Ver carrito
- `POST /carrito/agregar/<uuid>/` - Agregar al carrito
- `GET /carrito/eliminar/<uuid>/` - Eliminar del carrito
- `GET /carrito/vaciar/` - Vaciar carrito

### Órdenes
- `GET/POST /checkout/` - Finalizar compra
- `GET /orden/<uuid>/` - Detalle de orden

### API Interna
- `GET /api/lineas-por-grupo/<int>/` - Obtener líneas por grupo

## 📱 Capturas de Pantalla

### Dashboard Principal
El dashboard muestra estadísticas clave del negocio:
- Total de artículos en inventario
- Número de clientes registrados
- Órdenes pendientes de procesamiento
- Alertas de stock bajo

### Gestión de Artículos
Interfaz completa para:
- Crear y editar productos
- Asignar precios múltiples
- Controlar stock en tiempo real
- Organizar por categorías

### Sistema de Carrito
Experiencia de compra fluida:
- Agregar productos con un click
- Modificar cantidades fácilmente
- Calcular totales automáticamente
- Proceso de checkout intuitivo

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Sigue estos pasos:

### 1. Fork del Proyecto
```bash
git clone https://github.com/tu-usuario/sistema-pos.git
```

### 2. Crear Rama de Feature
```bash
git checkout -b feature/nueva-funcionalidad
```

### 3. Realizar Cambios
```bash
git commit -m "Agregar nueva funcionalidad increíble"
```

### 4. Push a la Rama
```bash
git push origin feature/nueva-funcionalidad
```

### 5. Crear Pull Request
- Describe claramente los cambios realizados
- Incluye tests si es necesario
- Actualiza la documentación

### Guías de Contribución
- Sigue las convenciones de código de Django
- Escribe tests para nuevas funcionalidades
- Documenta los cambios importantes
- Usa mensajes de commit descriptivos

## 🐛 Solución de Problemas

### Error de Migración
```bash
# Resetear migraciones
python reset_all_migrations.py
python manage.py migrate
```

### Error de Autenticación
```bash
# Recrear usuario administrador
python create_initial_user.py
```

### Error de Base de Datos
```bash
# Verificar conexión PostgreSQL
python manage.py dbshell
```

### Error de Archivos Estáticos
```bash
# Recolectar archivos estáticos
python manage.py collectstatic
```

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

- **Desarrollador**: Tu Nombre
- **Email**: tu.email@ejemplo.com
- **LinkedIn**: [tu-perfil](https://linkedin.com/in/tu-perfil)
- **GitHub**: [tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- **Django Community** - Por el excelente framework
- **Bootstrap Team** - Por los componentes UI
- **PostgreSQL** - Por la base de datos robusta
- **Font Awesome** - Por los iconos profesionales

---

⭐ **¡Si este proyecto te ayudó, considera darle una estrella!** ⭐

## 📈 Próximas Mejoras

- [ ] Sistema de reportes avanzados
- [ ] Integración con pasarelas de pago
- [ ] Aplicación móvil
- [ ] Sistema de notificaciones
- [ ] API REST completa
- [ ] Módulo de facturación
- [ ] Dashboard de analytics
- [ ] Integración con códigos QR
- [ ] Sistema de descuentos y promociones
- [ ] Módulo de contabilidad básica

## 🔄 Versionado

Utilizamos [SemVer](http://semver.org/) para el versionado. Para las versiones disponibles, consulta las [tags en este repositorio](https://github.com/tu-usuario/sistema-pos/tags).

**Versión Actual**: 1.0.0

---

**Desarrollado con ❤️ usando Django y Bootstrap**
