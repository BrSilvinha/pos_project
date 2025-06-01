# core/views.py - ARCHIVO COMPLETO Y CORREGIDO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import datetime
from decimal import Decimal
import uuid

# Para PDFs
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Importar modelos
from .models import (
    Articulo, GrupoArticulo, LineaArticulo, ListaPrecio,
    Cliente, Vendedor, OrdenCompraCliente, ItemOrdenCompraCliente,
    TipoIdentificacion, CanalCliente, Usuario
)
from pos_project.choices import EstadoOrden, EstadoEntidades
from .cart import Cart
from .forms import ArticuloForm, ListaPrecioForm

# ========================================
# VISTA DEL DASHBOARD
# ========================================

@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    
    try:
        total_articulos = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        total_clientes = Cliente.objects.filter(estado=EstadoEntidades.ACTIVO).count()
        ordenes_pendientes = OrdenCompraCliente.objects.filter(estado=EstadoOrden.PENDIENTE).count()
        bajo_stock = Articulo.objects.filter(stock__lt=10, estado=EstadoEntidades.ACTIVO).count()
    except Exception as e:
        messages.error(request, f'Error cargando estadísticas: {str(e)}')
        total_articulos = total_clientes = ordenes_pendientes = bajo_stock = 0
    
    context = {
        'total_articulos': total_articulos,
        'total_clientes': total_clientes,
        'ordenes_pendientes': ordenes_pendientes,
        'bajo_stock': bajo_stock,
    }
    
    return render(request, 'core/dashboard.html', context)

# ========================================
# VISTA DE PERFIL
# ========================================

@login_required
def profile_view(request):
    """Vista del perfil del usuario"""
    return render(request, 'accounts/profile.html')

# ========================================
# VISTAS DE ARTÍCULOS
# ========================================

@login_required
def articulos_list(request):
    """Vista para listar artículos con búsqueda y paginación"""
    
    try:
        # Usar select_related para optimizar consultas
        articulos_list = Articulo.objects.filter(
            estado=EstadoEntidades.ACTIVO
        ).select_related('grupo', 'linea').order_by('-fecha_creacion')
        
        # Búsqueda
        search_query = request.GET.get('q')
        if search_query:
            articulos_list = articulos_list.filter(
                Q(descripcion__icontains=search_query) |
                Q(codigo_articulo__icontains=search_query) |
                Q(codigo_barras__icontains=search_query)
            )
        
        # Filtro por stock bajo
        stock_filter = request.GET.get('stock')
        if stock_filter == 'bajo':
            articulos_list = articulos_list.filter(stock__lt=10)
        
        # Paginación
        paginator = Paginator(articulos_list, 12)
        page_number = request.GET.get('page')
        articulos = paginator.get_page(page_number)
        
    except Exception as e:
        messages.error(request, f'Error cargando artículos: {str(e)}')
        articulos = []
        search_query = ''
    
    context = {
        'articulos': articulos,
        'search_query': search_query,
    }
    
    return render(request, 'core/articulos/list.html', context)

@login_required
def articulo_detail(request, articulo_id):
    """Vista para ver detalle de un artículo"""
    
    try:
        articulo = get_object_or_404(
            Articulo.objects.select_related('grupo', 'linea'),
            articulo_id=articulo_id, 
            estado=EstadoEntidades.ACTIVO
        )
        
        # Productos relacionados (misma línea) - manejo seguro
        productos_relacionados = []
        if hasattr(articulo, 'linea') and articulo.linea:
            productos_relacionados = Articulo.objects.filter(
                linea=articulo.linea,
                estado=EstadoEntidades.ACTIVO
            ).exclude(articulo_id=articulo_id).select_related('grupo', 'linea')[:4]
        
    except Exception as e:
        messages.error(request, f'Error cargando artículo: {str(e)}')
        return redirect('articulos_list')
    
    context = {
        'articulo': articulo,
        'productos_relacionados': productos_relacionados,
    }
    
    return render(request, 'core/articulos/detail.html', context)
@login_required
def articulo_create(request):
    """Vista 100% segura para crear artículos"""
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario de manera manual y segura
            codigo_articulo = request.POST.get('codigo_articulo', '').strip()
            codigo_barras = request.POST.get('codigo_barras', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            presentacion = request.POST.get('presentacion', '').strip()
            grupo_id = request.POST.get('grupo', '')
            linea_id = request.POST.get('linea', '')
            stock = request.POST.get('stock', 0)
            precio_1 = request.POST.get('precio_1', 0)
            precio_2 = request.POST.get('precio_2', None)
            
            # Validaciones básicas
            if not codigo_articulo:
                messages.error(request, 'El código del artículo es obligatorio.')
                return redirect('articulo_create')
            
            if not descripcion:
                messages.error(request, 'La descripción es obligatoria.')
                return redirect('articulo_create')
            
            if not grupo_id:
                messages.error(request, 'Debe seleccionar un grupo.')
                return redirect('articulo_create')
            
            if not linea_id:
                messages.error(request, 'Debe seleccionar una línea.')
                return redirect('articulo_create')
            
            # Verificar que el código no exista
            if Articulo.objects.filter(codigo_articulo=codigo_articulo).exists():
                messages.error(request, 'Ya existe un artículo con ese código.')
                return redirect('articulo_create')
            
            # Obtener objetos relacionados
            try:
                grupo = GrupoArticulo.objects.get(grupo_id=grupo_id)
                linea = LineaArticulo.objects.get(linea_id=linea_id)
            except (GrupoArticulo.DoesNotExist, LineaArticulo.DoesNotExist):
                messages.error(request, 'Grupo o línea no válidos.')
                return redirect('articulo_create')
            
            # Crear el artículo de manera segura
            with transaction.atomic():
                articulo = Articulo.objects.create(
                    codigo_articulo=codigo_articulo,
                    codigo_barras=codigo_barras if codigo_barras else None,
                    descripcion=descripcion,
                    presentacion=presentacion if presentacion else None,
                    grupo=grupo,
                    linea=linea,
                    stock=int(stock) if stock else 0,
                    estado=EstadoEntidades.ACTIVO
                )
                
                # Crear precio
                ListaPrecio.objects.create(
                    articulo=articulo,
                    precio_1=float(precio_1) if precio_1 else 0,
                    precio_2=float(precio_2) if precio_2 else None,
                    estado=EstadoEntidades.ACTIVO
                )
                
                messages.success(request, f'Artículo "{articulo.descripcion}" creado exitosamente.')
                return redirect('articulo_detail', articulo_id=articulo.articulo_id)
        
        except Exception as e:
            messages.error(request, f'Error al crear artículo: {str(e)}')
            return redirect('articulo_create')
    
    # GET request - Renderizar formulario SIN OBJETOS PROBLEMÁTICOS
    try:
        # Obtener grupos activos
        grupos = list(GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).values(
            'grupo_id', 'nombre_grupo'
        ))
        
        # Si no hay grupos, crear uno por defecto
        if not grupos:
            grupo = GrupoArticulo.objects.create(
                nombre_grupo='General',
                estado=EstadoEntidades.ACTIVO
            )
            LineaArticulo.objects.create(
                nombre_linea='General',
                grupo=grupo,
                estado=EstadoEntidades.ACTIVO
            )
            grupos = list(GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).values(
                'grupo_id', 'nombre_grupo'
            ))
            messages.info(request, 'Se creó un grupo "General" por defecto.')
        
    except Exception as e:
        messages.error(request, f'Error cargando grupos: {str(e)}')
        grupos = []
    
    # Contexto 100% seguro - SIN OBJETOS ARTICULO
    context = {
        'grupos': grupos,
        'edit_mode': False,  # Modo creación
        'articulo': None,    # IMPORTANTE: No pasar ningún objeto artículo
        'form_data': {},     # Datos vacíos para el formulario
    }
    
    # Usar template simple y seguro
    return render(request, 'articulos/crear.html', context)

@login_required
def articulo_edit(request, articulo_id):
    """Vista para editar un artículo - CORREGIDA"""
    
    try:
        articulo = get_object_or_404(
            Articulo.objects.select_related('grupo', 'linea'),
            articulo_id=articulo_id
        )
        
        # Obtener precio de forma segura
        precio = None
        try:
            precio = articulo.precios.first()
        except:
            pass
        
    except Exception as e:
        messages.error(request, f'Error cargando artículo: {str(e)}')
        return redirect('articulos_list')
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=precio)
        
        if form.is_valid() and precio_form.is_valid():
            try:
                with transaction.atomic():
                    # Actualizar el artículo
                    articulo = form.save()
                    
                    # Actualizar o crear el precio
                    if precio:
                        precio_form.save()
                    else:
                        nuevo_precio = precio_form.save(commit=False)
                        nuevo_precio.articulo = articulo
                        nuevo_precio.save()
                    
                    messages.success(request, f'Artículo "{articulo.descripcion}" actualizado exitosamente.')
                    return redirect('articulo_detail', articulo_id=articulo.articulo_id)
                    
            except Exception as e:
                messages.error(request, f'Error al actualizar el artículo: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ArticuloForm(instance=articulo)
        precio_form = ListaPrecioForm(instance=precio)
    
    # Obtener grupos activos
    try:
        grupos = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO).order_by('nombre_grupo')
    except Exception as e:
        messages.error(request, f'Error cargando grupos: {str(e)}')
        grupos = []
    
    context = {
        'form': form,
        'precio_form': precio_form,
        'articulo': articulo,
        'grupos': grupos,
        'edit_mode': True,
    }
    
    return render(request, 'core/articulos/form.html', context)

@login_required
def articulo_delete(request, articulo_id):
    """Vista para eliminar un artículo"""
    
    try:
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('articulos_list')
    
    if request.method == 'POST':
        try:
            articulo.estado = EstadoEntidades.INACTIVO
            articulo.save()
            messages.success(request, f'Artículo "{articulo.descripcion}" eliminado exitosamente.')
            return redirect('articulos_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el artículo: {str(e)}')
    
    context = {
        'articulo': articulo,
    }
    
    return render(request, 'core/articulos/delete.html', context)

# ========================================
# VISTAS DEL CARRITO
# ========================================

@login_required
def cart_detail(request):
    """Vista para mostrar el carrito"""
    cart = Cart(request)
    return render(request, 'core/cart/detail.html', {'cart': cart})

@login_required
@require_POST
def cart_add(request, articulo_id):
    """Vista para agregar productos al carrito"""
    
    try:
        cart = Cart(request)
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
        
        cantidad = int(request.POST.get('cantidad', 1))
        update_cantidad = request.POST.get('update', False)
        
        if cantidad > articulo.stock:
            messages.error(request, f'Stock insuficiente. Disponible: {articulo.stock}')
        else:
            cart.add(articulo=articulo, cantidad=cantidad, update_cantidad=bool(update_cantidad))
            
            if update_cantidad:
                messages.success(request, 'Carrito actualizado.')
            else:
                messages.success(request, f'"{articulo.descripcion}" agregado al carrito.')
                
    except ValueError:
        messages.error(request, 'Cantidad inválida.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('cart_detail')

@login_required
def cart_remove(request, articulo_id):
    """Vista para eliminar productos del carrito"""
    
    try:
        cart = Cart(request)
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
        
        cart.remove(articulo)
        messages.success(request, f'"{articulo.descripcion}" eliminado del carrito.')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('cart_detail')

@login_required
def cart_clear(request):
    """Vista para vaciar el carrito"""
    
    try:
        cart = Cart(request)
        cart.clear()
        messages.success(request, 'Carrito vaciado.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('cart_detail')

# ========================================
# VISTAS DE CHECKOUT Y ÓRDENES
# ========================================

@login_required
def checkout(request):
    """Vista para finalizar la compra"""
    
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('cart_detail')
    
    # Obtener o crear cliente basado en el usuario actual
    try:
        tipo_id = TipoIdentificacion.objects.filter(estado=EstadoEntidades.ACTIVO).first()
        canal = CanalCliente.objects.filter(estado=EstadoEntidades.ACTIVO).first()
        
        if not tipo_id:
            # Crear tipo de identificación por defecto
            tipo_id = TipoIdentificacion.objects.create(
                nombre_tipo_identificacion='DNI',
                estado=EstadoEntidades.ACTIVO
            )
        
        if not canal:
            # Crear canal por defecto
            canal = CanalCliente.objects.create(
                nombre_canal='Presencial',
                estado=EstadoEntidades.ACTIVO
            )
        
        cliente, created = Cliente.objects.get_or_create(
            correo_electronico=request.user.email,
            defaults={
                'nombres': request.user.full_name or request.user.username,
                'nro_documento': '00000000',
                'tipo_identificacion': tipo_id,
                'canal': canal,
                'estado': EstadoEntidades.ACTIVO
            }
        )
        
    except Exception as e:
        messages.error(request, f'Error al procesar cliente: {str(e)}')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        try:
            # Obtener o crear vendedor
            vendedor = Vendedor.objects.filter(estado=EstadoEntidades.ACTIVO).first()
            if not vendedor:
                vendedor = Vendedor.objects.create(
                    nombres='Vendedor Predeterminado',
                    correo_electronico='vendedor@sistema.com',
                    estado=EstadoEntidades.ACTIVO
                )
            
            with transaction.atomic():
                # Crear la orden
                orden = OrdenCompraCliente.objects.create(
                    cliente=cliente,
                    vendedor=vendedor,
                    estado=EstadoOrden.PENDIENTE,
                    notas=request.POST.get('notas', ''),
                    creado_por=request.user
                )
                
                # Crear los items de la orden
                item_numero = 1
                for item in cart:
                    ItemOrdenCompraCliente.objects.create(
                        pedido=orden,
                        nro_item=item_numero,
                        articulo=item['articulo'],
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio'],
                        creado_por=request.user
                    )
                    
                    # Actualizar stock
                    articulo = item['articulo']
                    articulo.stock -= item['cantidad']
                    articulo.save()
                    
                    item_numero += 1
                
                # Actualizar total de la orden
                orden.actualizar_total()
                
                # Limpiar carrito
                cart.clear()
                
                messages.success(request, f'¡Orden #{orden.nro_pedido} creada exitosamente!')
                return redirect('order_detail', pedido_id=orden.pedido_id)
            
        except Exception as e:
            messages.error(request, f'Error al procesar la orden: {str(e)}')
            return redirect('cart_detail')
    
    context = {
        'cart': cart,
        'cliente': cliente,
    }
    
    return render(request, 'core/cart/checkout.html', context)

@login_required
def order_detail(request, pedido_id):
    """Vista para ver detalle de una orden"""
    
    try:
        orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
        
        # Verificar que el usuario puede ver esta orden
        if not request.user.is_staff and orden.cliente.correo_electronico != request.user.email:
            messages.error(request, 'No tienes permiso para ver esta orden.')
            return redirect('dashboard')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')
    
    context = {
        'orden': orden,
    }
    
    return render(request, 'core/cart/order_detail.html', context)

@login_required
def order_list(request):
    """Vista para listar órdenes de compra"""
    
    try:
        if request.user.is_staff:
            ordenes_list = OrdenCompraCliente.objects.all().order_by('-fecha_creacion')
        else:
            clientes = Cliente.objects.filter(correo_electronico=request.user.email)
            ordenes_list = OrdenCompraCliente.objects.filter(cliente__in=clientes).order_by('-fecha_creacion')
        
        # Filtros
        estado = request.GET.get('estado')
        if estado and estado.isdigit():
            ordenes_list = ordenes_list.filter(estado=int(estado))
        
        fecha_desde = request.GET.get('fecha_desde')
        if fecha_desde:
            try:
                fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                ordenes_list = ordenes_list.filter(fecha_pedido__gte=fecha_desde)
            except:
                pass
        
        fecha_hasta = request.GET.get('fecha_hasta')
        if fecha_hasta:
            try:
                fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                ordenes_list = ordenes_list.filter(fecha_pedido__lte=fecha_hasta)
            except:
                pass
        
        # Paginación
        paginator = Paginator(ordenes_list, 10)
        page_number = request.GET.get('page')
        ordenes = paginator.get_page(page_number)
        
    except Exception as e:
        messages.error(request, f'Error cargando órdenes: {str(e)}')
        ordenes = []
        estado = fecha_desde = fecha_hasta = None
    
    context = {
        'ordenes': ordenes,
        'estados': EstadoOrden.choices,
        'filtros': {
            'estado': estado,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
    }
    
    return render(request, 'core/cart/order_list.html', context)

@login_required
def cancel_order(request, pedido_id):
    """Cancelar una orden"""
    
    try:
        orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
        
        if request.user.is_staff or orden.cliente.correo_electronico == request.user.email:
            if orden.estado == EstadoOrden.PENDIENTE:
                with transaction.atomic():
                    orden.estado = EstadoOrden.CANCELADA
                    orden.save()
                    
                    # Restaurar stock
                    for item in orden.items_orden_compra.all():
                        articulo = item.articulo
                        articulo.stock += item.cantidad
                        articulo.save()
                
                messages.success(request, f'Orden #{orden.nro_pedido} cancelada correctamente.')
            else:
                messages.error(request, 'Solo se pueden cancelar órdenes pendientes.')
        else:
            messages.error(request, 'No tienes permiso para cancelar esta orden.')
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('order_list')

# ========================================
# API ENDPOINTS
# ========================================

@login_required
def lineas_por_grupo(request, grupo_id):
    """API endpoint para obtener líneas por grupo"""
    try:
        lineas = LineaArticulo.objects.filter(
            grupo_id=grupo_id, 
            estado=EstadoEntidades.ACTIVO
        ).values('linea_id', 'nombre_linea')
        
        data = [{'id': linea['linea_id'], 'nombre': linea['nombre_linea']} for linea in lineas]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ========================================
# FUNCIONES DE PDF
# ========================================

@login_required
def generate_pdf_order(request, pedido_id):
    """Generar PDF para una orden usando ReportLab"""
    
    try:
        orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
        
        # Verificar que el usuario puede acceder a esta orden
        if not request.user.is_staff and orden.cliente.correo_electronico != request.user.email:
            messages.error(request, 'No tienes permiso para ver esta orden.')
            return redirect('dashboard')
        
        # Crear un buffer para el PDF
        buffer = BytesIO()
        
        # Crear el PDF
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Título
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, height - 50, f"Orden de Compra #{orden.nro_pedido}")
        
        # Fecha
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, f"Fecha: {orden.fecha_pedido}")
        
        # Estado
        estado_display = dict(EstadoOrden.choices).get(orden.estado, "Desconocido")
        p.drawString(50, height - 100, f"Estado: {estado_display}")
        
        # Información del cliente
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, "Información del Cliente:")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 160, f"Nombre: {orden.cliente.nombres}")
        p.drawString(50, height - 180, f"Documento: {orden.cliente.tipo_identificacion.nombre_tipo_identificacion} {orden.cliente.nro_documento}")
        p.drawString(50, height - 200, f"Email: {orden.cliente.correo_electronico}")
        
        # Tabla de items
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 240, "Detalle de la Orden:")
        
        # Items de la orden
        y = height - 280
        p.setFont("Helvetica", 10)
        p.drawString(50, y, "Item")
        p.drawString(150, y, "Producto")
        p.drawString(350, y, "Precio")
        p.drawString(420, y, "Cantidad")
        p.drawString(490, y, "Total")
        
        y -= 20
        for item in orden.items_orden_compra.all():
            p.drawString(50, y, str(item.nro_item))
            p.drawString(150, y, item.articulo.descripcion[:25])
            p.drawString(350, y, f"${item.precio_unitario}")
            p.drawString(420, y, str(item.cantidad))
            p.drawString(490, y, f"${item.total_item}")
            y -= 15
        
        # Total
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(420, y, f"Total: ${orden.importe}")
        
        # Pie de página
        p.setFont("Helvetica", 10)
        p.drawString(50, 50, f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
        p.drawString(width - 200, 50, "Sistema POS © 2025")
        
        # Guardar el PDF
        p.showPage()
        p.save()
        
        # Preparar la respuesta
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="orden_{orden.nro_pedido}.pdf"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error generando PDF: {str(e)}')
        return redirect('order_detail', pedido_id=pedido_id)

# ========================================
# FUNCIONES DE EMAIL (OPCIONAL)
# ========================================

def send_order_confirmation_email(orden):
    """Enviar email de confirmación de orden"""
    try:
        subject = f'Confirmación de Orden #{orden.nro_pedido}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = orden.cliente.correo_electronico
        
        # Renderizar el cuerpo del email en HTML
        html_content = render_to_string('emails/order_confirmation.html', {
            'orden': orden,
            'items': orden.items_orden_compra.all(),
        })
        
        # Versión de texto plano
        text_content = strip_tags(html_content)
        
        # Crear el mensaje
        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [to_email]
        )
        
        # Adjuntar versión HTML
        email.attach_alternative(html_content, "text/html")
        
        # Enviar el email
        email.send()
        return True
    except Exception as e:
        print(f"Error enviando email: {str(e)}")
        return False