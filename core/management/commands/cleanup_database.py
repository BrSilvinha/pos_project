# core/management/commands/cleanup_database.py
# Crear este archivo en: core/management/commands/cleanup_database.py

from django.core.management.base import BaseCommand
from django.db import connection
from core.models import *
import uuid

class Command(BaseCommand):
    help = 'Limpia y verifica datos inconsistentes en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Corrige automáticamente los datos inconsistentes',
        )

    def handle(self, *args, **options):
        fix_data = options['fix']
        
        self.stdout.write(self.style.WARNING('Verificando base de datos...'))
        
        # 1. Verificar datos con UUIDs inválidos
        try:
            with connection.cursor() as cursor:
                # Verificar tabla de artículos
                cursor.execute("SELECT COUNT(*) FROM articulos WHERE articulo_id = '1' OR articulo_id = '0'")
                invalid_articulos = cursor.fetchone()[0]
                
                if invalid_articulos > 0:
                    self.stdout.write(
                        self.style.ERROR(f'Encontrados {invalid_articulos} artículos con UUID inválido')
                    )
                    
                    if fix_data:
                        cursor.execute("DELETE FROM articulos WHERE articulo_id = '1' OR articulo_id = '0'")
                        self.stdout.write(self.style.SUCCESS('Artículos con UUID inválido eliminados'))
                
                # Verificar tabla de clientes
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE cliente_id = '1' OR cliente_id = '0'")
                invalid_clientes = cursor.fetchone()[0]
                
                if invalid_clientes > 0:
                    self.stdout.write(
                        self.style.ERROR(f'Encontrados {invalid_clientes} clientes con UUID inválido')
                    )
                    
                    if fix_data:
                        cursor.execute("DELETE FROM clientes WHERE cliente_id = '1' OR cliente_id = '0'")
                        self.stdout.write(self.style.SUCCESS('Clientes con UUID inválido eliminados'))
                
                # Verificar tabla de usuarios
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario_id = '1' OR usuario_id = '0'")
                invalid_usuarios = cursor.fetchone()[0]
                
                if invalid_usuarios > 0:
                    self.stdout.write(
                        self.style.ERROR(f'Encontrados {invalid_usuarios} usuarios con UUID inválido')
                    )
                    
                    if fix_data:
                        cursor.execute("DELETE FROM usuarios WHERE usuario_id = '1' OR usuario_id = '0'")
                        self.stdout.write(self.style.SUCCESS('Usuarios con UUID inválido eliminados'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error verificando UUIDs: {e}'))
        
        # 2. Verificar datos básicos necesarios
        try:
            # Verificar tipos de identificación
            tipos_id = TipoIdentificacion.objects.count()
            if tipos_id == 0:
                self.stdout.write(self.style.WARNING('No hay tipos de identificación'))
                if fix_data:
                    TipoIdentificacion.objects.create(
                        nombre_tipo_identificacion='DNI',
                        estado=1
                    )
                    TipoIdentificacion.objects.create(
                        nombre_tipo_identificacion='RUC',
                        estado=1
                    )
                    self.stdout.write(self.style.SUCCESS('Tipos de identificación creados'))
            
            # Verificar canales de cliente
            canales = CanalCliente.objects.count()
            if canales == 0:
                self.stdout.write(self.style.WARNING('No hay canales de cliente'))
                if fix_data:
                    CanalCliente.objects.create(
                        nombre_canal='Presencial',
                        estado=1
                    )
                    CanalCliente.objects.create(
                        nombre_canal='Online',
                        estado=1
                    )
                    self.stdout.write(self.style.SUCCESS('Canales de cliente creados'))
            
            # Verificar vendedores
            vendedores = Vendedor.objects.count()
            if vendedores == 0:
                self.stdout.write(self.style.WARNING('No hay vendedores'))
                if fix_data:
                    Vendedor.objects.create(
                        nombres='Vendedor Predeterminado',
                        correo_electronico='vendedor@sistema.com',
                        estado=1
                    )
                    self.stdout.write(self.style.SUCCESS('Vendedor predeterminado creado'))
            
            # Verificar grupos de artículos
            grupos = GrupoArticulo.objects.count()
            if grupos == 0:
                self.stdout.write(self.style.WARNING('No hay grupos de artículos'))
                if fix_data:
                    grupo = GrupoArticulo.objects.create(
                        nombre_grupo='General',
                        estado=1
                    )
                    LineaArticulo.objects.create(
                        nombre_linea='General',
                        grupo=grupo,
                        estado=1
                    )
                    self.stdout.write(self.style.SUCCESS('Grupo y línea predeterminados creados'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error verificando datos básicos: {e}'))
        
        # 3. Mostrar estadísticas actuales
        try:
            stats = {
                'Artículos': Articulo.objects.count(),
                'Clientes': Cliente.objects.count(),
                'Usuarios': Usuario.objects.count(),
                'Vendedores': Vendedor.objects.count(),
                'Grupos': GrupoArticulo.objects.count(),
                'Líneas': LineaArticulo.objects.count(),
                'Tipos ID': TipoIdentificacion.objects.count(),
                'Canales': CanalCliente.objects.count(),
            }
            
            self.stdout.write(self.style.SUCCESS('\n=== ESTADÍSTICAS ACTUALES ==='))
            for nombre, cantidad in stats.items():
                self.stdout.write(f'{nombre}: {cantidad}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error obteniendo estadísticas: {e}'))
        
        if not fix_data:
            self.stdout.write(
                self.style.WARNING('\nPara corregir automáticamente los problemas, ejecuta:')
            )
            self.stdout.write('python manage.py cleanup_database --fix')
        else:
            self.stdout.write(self.style.SUCCESS('\n¡Limpieza completada!'))