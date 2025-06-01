# core/views.py - Archivo completo con todas las vistas

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import datetime

# Para PDFs
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Para WeasyPrint
try:
    from weasyprint import HTML
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

import tempfile
import os

from .models import (
    Articulo, GrupoArticulo, LineaArticulo, ListaPrecio,
    Cliente, Vendedor, OrdenCompraCliente, ItemOrdenCompraCliente,
    TipoIdentificacion, CanalCliente, Usuario
)
from pos_project.choices import EstadoOrden, EstadoEntidades
from .cart import Cart
from .forms import ArticuloForm, ListaPrecioForm
import uuid

# ========================================
# VISTA DEL DASHBOARD
# ========================================

@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    
    # Estadísticas generales
    total_articulos = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count()
    total_clientes = Cliente.objects.filter(estado=EstadoEntidades.ACTIVO).count()
    ordenes_pendientes = OrdenCompraCliente.objects.filter(estado=EstadoOrden.PENDIENTE).count()
    bajo_stock = Articulo.objects.filter(stock__lt=10, estado=EstadoEntidades.ACTIVO).count()
    
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
    
    # Obtener todos los artículos activos
    articulos_list = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).order_by('-fecha_creacion')
    
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
    paginator = Paginator(articulos_list, 12)  # 12 artículos por página
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)
    
    context = {
        'articulos': articulos,
        'search_query': search_query,
    }
    
    return render(request, 'core/articulos/list.html', context)

@login_required
def articulo_detail(request, articulo_id):
    """Vista para ver detalle de un artículo"""
    
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id, estado=EstadoEntidades.ACTIVO)
    
    # Productos relacionados (misma línea)
    productos_relacionados = Articulo.objects.filter(
        linea=articulo.linea,
        estado=EstadoEntidades.ACTIVO
    ).exclude(articulo_id=articulo_id)[:4]
    
    context = {
        'articulo': articulo,
        'productos_relacionados': productos_relacionados,
    }
    
    return render(request, 'core/articulos/detail.html', context)

@login_required
def articulo_create(request):
    """Vista para crear un nuevo artículo"""
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        precio_form = ListaPrecioForm(request.POST)
        
        if form.is_valid() and precio_form.is_valid():
            try:
                # Guardar el artículo
                articulo = form.save()
                
                # Guardar el precio
                precio = precio_form.save(commit=False)
                precio.articulo = articulo
                precio.save()
                
                messages.success(request, f'Artículo "{articulo.descripcion}" creado exitosamente.')
                return redirect('articulo_detail', articulo_id=articulo.articulo_id)
                
            except Exception as e:
                messages.error(request, f'Error al crear el artículo: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ArticuloForm()
        precio_form = ListaPrecioForm()
    
    context = {
        'form': form,
        'precio_form': precio_form,
    }
    
    return render(request, 'core/articulos/form.html', context)

@login_required
def articulo_edit(request, articulo_id):
    """Vista para editar un artículo"""
    
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    precio = articulo.precios.first()
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=precio)
        
        if form.is_valid() and precio_form.is_valid():
            try:
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
    
    context = {
        'form': form,
        'precio_form': precio_form,
        'articulo': articulo,
    }
    
    return render(request, 'core/articulos/form.html', context)

@login_required
def articulo_delete(request, articulo_id):
    """Vista para eliminar un artículo"""
    
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    
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
    
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    
    try:
        cantidad = int(request.POST.get('cantidad', 1))
        update_cantidad = request.POST.get('update', False)
        
        # Validar stock disponible
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
    
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    
    cart.remove(articulo)
    messages.success(request, f'"{articulo.descripcion}" eliminado del carrito.')
    
    return redirect('cart_detail')

@login_required
def cart_clear(request):
    """Vista para vaciar el carrito"""
    
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Carrito vaciado.')
    
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
        
        if not tipo_id or not canal:
            messages.error(request, 'Configuración incompleta. Contacta al administrador.')
            return redirect('cart_detail')
        
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
            # Obtener vendedor predeterminado
            vendedor = Vendedor.objects.filter(estado=EstadoEntidades.ACTIVO).first()
            if not vendedor:
                messages.error(request, 'No hay vendedores disponibles.')
                return redirect('cart_detail')
            
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
            
            # Enviar email de confirmación
            try:
                send_order_confirmation_email(orden)
                messages.success(request, f'¡Orden #{orden.nro_pedido} creada exitosamente! Se ha enviado un email de confirmación.')
            except Exception as e:
                messages.warning(request, f'Orden creada pero no se pudo enviar email: {str(e)}')
            
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
    
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
    
    # Verificar que el usuario puede ver esta orden
    if not request.user.is_staff and orden.cliente.correo_electronico != request.user.email:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('dashboard')
    
    context = {
        'orden': orden,
    }
    
    return render(request, 'core/cart/order_detail.html', context)

@login_required
def order_list(request):
    """Vista para listar órdenes de compra"""
    
    # Determinar si el usuario es staff (puede ver todas las órdenes) o no (solo ve las suyas)
    if request.user.is_staff:
        ordenes_list = OrdenCompraCliente.objects.all().order_by('-fecha_creacion')
    else:
        # Buscar cliente asociado al usuario actual
        try:
            clientes = Cliente.objects.filter(correo_electronico=request.user.email)
            ordenes_list = OrdenCompraCliente.objects.filter(cliente__in=clientes).order_by('-fecha_creacion')
        except:
            messages.error(request, "No se encontraron órdenes asociadas a tu cuenta.")
            return redirect('dashboard')
    
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
    paginator = Paginator(ordenes_list, 10)  # 10 órdenes por página
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    # Contexto
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
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
    
    # Verificar que el usuario puede modificar esta orden
    if request.user.is_staff or orden.cliente.correo_electronico == request.user.email:
        # Solo se pueden cancelar órdenes pendientes
        if orden.estado == EstadoOrden.PENDIENTE:
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
# FUNCIONES DE EMAIL
# ========================================

def send_order_confirmation_email(orden):
    """
    Enviar email de confirmación de orden
    """
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

# ========================================
# FUNCIONES DE PDF - REPORTLAB
# ========================================

@login_required
def generate_pdf_order(request, pedido_id):
    """Generar PDF para una orden usando ReportLab"""
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
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Título
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, height - 50, f"Orden de Compra #{orden.nro_pedido}")
    
    # Fecha
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 80, f"Fecha: {orden.fecha_pedido}")
    
    # Estado
    p.setFont("Helvetica", 12)
    estado_display = "Pendiente" if orden.estado == 1 else "Procesando" if orden.estado == 2 else "Completada" if orden.estado == 3 else "Cancelada"
    p.drawString(50, height - 100, f"Estado: {estado_display}")
    
    # Información del cliente
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 140, "Información del Cliente:")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Nombre: {orden.cliente.nombres}")
    p.drawString(50, height - 180, f"Documento: {orden.cliente.tipo_identificacion.nombre_tipo_identificacion} {orden.cliente.nro_documento}")
    p.drawString(50, height - 200, f"Email: {orden.cliente.correo_electronico}")
    
    if orden.cliente.direccion:
        # Manejar direcciones largas
        direccion = orden.cliente.direccion
        if len(direccion) > 60:
            direccion1 = direccion[:60]
            direccion2 = direccion[60:]
            p.drawString(50, height - 220, f"Dirección: {direccion1}")
            p.drawString(110, height - 240, f"{direccion2}")
        else:
            p.drawString(50, height - 220, f"Dirección: {direccion}")
    
    # Tabla de items
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 280, "Detalle de la Orden:")
    
    # Crear datos de la tabla
    data = [['#', 'Producto', 'Precio', 'Cantidad', 'Total']]
    
    for item in orden.items_orden_compra.all():
        data.append([
            str(item.nro_item),
            item.articulo.descripcion,
            f"${item.precio_unitario}",
            str(item.cantidad),
            f"${item.total_item}"
        ])
    
    # Añadir fila de total
    data.append(['', '', '', 'Total:', f"${orden.importe}"])
    
    # Crear la tabla
    table = Table(data, colWidths=[30, 250, 70, 70, 70])
    
    # Estilo de la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (3, -1), (-1, -1), 'RIGHT'),
    ]))
    
    # Dibujar la tabla
    table.wrapOn(p, width - 100, height)
    table.drawOn(p, 50, height - 500)
    
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

# ========================================
# FUNCIONES DE PDF - WEASYPRINT
# ========================================

@login_required
def generate_pdf_order_weasy(request, pedido_id):
    """Generar PDF para una orden usando WeasyPrint (HTML a PDF)"""
    if not WEASYPRINT_AVAILABLE:
        messages.error(request, 'WeasyPrint no está disponible. Usa la versión ReportLab.')
        return redirect('generate_pdf_order', pedido_id=pedido_id)
    
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
    
    # Verificar que el usuario puede acceder a esta orden
    if not request.user.is_staff and orden.cliente.correo_electronico != request.user.email:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('dashboard')
    
    # Renderizar el HTML
    html_string = render_to_string('pdf/order_template.html', {
        'orden': orden,
        'items': orden.items_orden_compra.all(),
        'fecha_generacion': timezone.now(),
    })
    
    # Configuración de fuentes
    font_config = FontConfiguration()
    
    # Crear el PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    result = html.write_pdf(font_config=font_config)
    
    # Crear respuesta HTTP
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="orden_{orden.nro_pedido}.pdf"'
    
    return response