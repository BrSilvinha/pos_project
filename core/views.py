# core/views.py - Agregar estas importaciones al inicio del archivo

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
import uuid

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
    if orden.cliente.correo_electronico != request.user.email and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('home')
    
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
    if orden.cliente.correo_electronico != request.user.email and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('home')
    
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

# ========================================
# LISTADO DE ÓRDENES
# ========================================

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
            return redirect('home')
    
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
            messages.success(request, f'Orden #{orden.nro_pedido} cancelada correctamente.')
        else:
            messages.error(request, 'Solo se pueden cancelar órdenes pendientes.')
    else:
        messages.error(request, 'No tienes permiso para cancelar esta orden.')
    
    return redirect('order_list')

# ========================================
# MODIFICAR FUNCIÓN CHECKOUT EXISTENTE
# ========================================

# Encuentra tu función checkout existente y reemplaza la parte donde se crea la orden
# con este código para incluir el envío de email:

# En la función checkout, después de crear la orden exitosamente, agregar:
"""
# Después de crear la orden e items, agregar esta línea:
try:
    send_order_confirmation_email(orden)
    messages.success(request, f'¡Orden creada exitosamente! Tu número de orden es: {orden.nro_pedido}. Se ha enviado un email de confirmación.')
except Exception as e:
    messages.warning(request, f'Orden creada pero no se pudo enviar el email de confirmación: {str(e)}')
"""