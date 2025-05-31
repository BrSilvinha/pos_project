# core/views.py - Vista dashboard corregida

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Articulo, GrupoArticulo, LineaArticulo, ListaPrecio,
    Cliente, Vendedor, OrdenCompraCliente, ItemOrdenCompraCliente,
    TipoIdentificacion, CanalCliente, Usuario
)
from pos_project.choices import EstadoOrden, EstadoEntidades
from .cart import Cart
import uuid

@login_required
def dashboard(request):
    """Vista principal del dashboard con manejo de errores"""
    try:
        # Consultas con manejo de errores
        total_articulos = Articulo.objects.filter(estado=1).count()  # Usar valor entero directamente
        total_clientes = Cliente.objects.filter(estado=1).count()
        ordenes_pendientes = OrdenCompraCliente.objects.filter(estado=1).count()
        
        # Estadísticas adicionales para el template
        total_usuarios = Usuario.objects.filter(is_active=True).count()
        
        # Artículos con bajo stock (menos de 10 unidades)
        bajo_stock = Articulo.objects.filter(estado=1, stock__lt=10).count()
        
        # Ventas de hoy (simulado por ahora)
        ventas_hoy = 0  # Puedes implementar esta lógica más tarde
        
        context = {
            'total_articulos': total_articulos,
            'total_clientes': total_clientes,
            'ordenes_pendientes': ordenes_pendientes,
            'total_usuarios': total_usuarios,
            'bajo_stock': bajo_stock,
            'ventas_hoy': ventas_hoy,
        }
        
    except Exception as e:
        # Si hay error, mostrar mensaje y valores por defecto
        messages.error(request, f'Error al cargar estadísticas: {str(e)}')
        context = {
            'total_articulos': 0,
            'total_clientes': 0,
            'ordenes_pendientes': 0,
            'total_usuarios': 0,
            'bajo_stock': 0,
            'ventas_hoy': 0,
        }
    
    return render(request, 'core/dashboard.html', context)

@login_required
def articulos_list(request):
    """Vista para listar artículos con paginación"""
    try:
        articulos_list = Articulo.objects.filter(estado=1).select_related('grupo', 'linea')
        
        # Filtros
        q = request.GET.get('q')
        if q:
            articulos_list = articulos_list.filter(
                Q(descripcion__icontains=q) | 
                Q(codigo_articulo__icontains=q)
            )
        
        # Filtro de stock bajo
        stock_filter = request.GET.get('stock')
        if stock_filter == 'bajo':
            articulos_list = articulos_list.filter(stock__lt=10)
        
        # Paginación
        paginator = Paginator(articulos_list, 15)
        page_number = request.GET.get('page')
        articulos = paginator.get_page(page_number)
        
        context = {
            'articulos': articulos,
            'search_query': q,
        }
        return render(request, 'core/articulos/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar artículos: {str(e)}')
        return redirect('dashboard')

@login_required
def articulo_detail(request, articulo_id):
    """Vista para ver el detalle de un artículo"""
    try:
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
        
        # Guardar en el historial de productos visitados
        if 'viewed_products' not in request.session:
            request.session['viewed_products'] = []
        
        # Convertir UUID a string para poder guardarlo en sesión
        producto_actual = str(articulo.articulo_id)
        viewed_products = request.session['viewed_products']
        
        # Eliminar si ya existe y añadir al principio
        if producto_actual in viewed_products:
            viewed_products.remove(producto_actual)
        
        # Añadir al principio y mantener solo los últimos 5
        viewed_products.insert(0, producto_actual)
        request.session['viewed_products'] = viewed_products[:5]
        request.session.modified = True
        
        # Obtener productos visitados recientemente
        recent_products = []
        if viewed_products:
            try:
                recent_uuids = [uuid.UUID(id_str) for id_str in viewed_products[1:6]]  # Excluir el actual
                if recent_uuids:
                    recent_products = Articulo.objects.filter(
                        articulo_id__in=recent_uuids,
                        estado=1
                    )
            except (ValueError, TypeError):
                # Si hay problemas con los UUIDs en sesión, limpiar
                request.session['viewed_products'] = []
        
        context = {
            'articulo': articulo,
            'recent_products': recent_products,
        }
        return render(request, 'core/articulos/detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al cargar artículo: {str(e)}')
        return redirect('articulos_list')

# API para obtener líneas por grupo
def lineas_por_grupo(request, grupo_id):
    """API para obtener líneas de artículo por grupo"""
    try:
        lineas = LineaArticulo.objects.filter(
            grupo_id=grupo_id, 
            estado=1
        ).values('linea_id', 'nombre_linea')
        return JsonResponse(list(lineas), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# VISTAS DEL CARRITO DE COMPRAS

@require_POST
def cart_add(request, articulo_id):
    """Añadir artículo al carrito"""
    try:
        cart = Cart(request)
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
        cantidad = int(request.POST.get('cantidad', 1))
        update = request.POST.get('update')
        
        cart.add(articulo=articulo, cantidad=cantidad, update_cantidad=update)
        messages.success(request, f'"{articulo.descripcion}" añadido al carrito.')
        
        return redirect('cart_detail')
        
    except Exception as e:
        messages.error(request, f'Error al añadir al carrito: {str(e)}')
        return redirect('articulos_list')

def cart_remove(request, articulo_id):
    """Eliminar artículo del carrito"""
    try:
        cart = Cart(request)
        articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
        cart.remove(articulo)
        messages.info(request, f'"{articulo.descripcion}" eliminado del carrito.')
        
        return redirect('cart_detail')
        
    except Exception as e:
        messages.error(request, f'Error al eliminar del carrito: {str(e)}')
        return redirect('cart_detail')

def cart_detail(request):
    """Ver detalle del carrito"""
    cart = Cart(request)
    return render(request, 'core/cart/detail.html', {'cart': cart})

def cart_clear(request):
    """Vaciar el carrito"""
    try:
        cart = Cart(request)
        cart.clear()
        messages.info(request, 'Carrito vaciado correctamente.')
        
    except Exception as e:
        messages.error(request, f'Error al vaciar carrito: {str(e)}')
    
    return redirect('cart_detail')

@login_required
def checkout(request):
    """Finalizar compra"""
    try:
        cart = Cart(request)
        
        if len(cart) == 0:
            messages.warning(request, 'Tu carrito está vacío')
            return redirect('cart_detail')
        
        # Obtener o crear cliente para el usuario
        try:
            cliente = Cliente.objects.get(correo_electronico=request.user.email)
        except Cliente.DoesNotExist:
            # Obtener tipo de identificación predeterminado
            try:
                tipo_id = TipoIdentificacion.objects.first()
                canal = CanalCliente.objects.first()
                
                if not tipo_id or not canal:
                    messages.error(request, 'Configuración incompleta. Contacte al administrador.')
                    return redirect('cart_detail')
                
                # Crear cliente con datos básicos del usuario
                cliente = Cliente.objects.create(
                    cliente_id=uuid.uuid4(),
                    tipo_identificacion=tipo_id,
                    nro_documento=request.user.username[:11],
                    nombres=request.user.full_name or request.user.username,
                    correo_electronico=request.user.email,
                    canal=canal,
                    estado=1
                )
            except Exception as e:
                messages.error(request, f'Error al procesar el cliente: {str(e)}')
                return redirect('cart_detail')
        
        # Obtener vendedor predeterminado para la orden
        try:
            vendedor = Vendedor.objects.first()
            if not vendedor:
                messages.error(request, 'No hay vendedores disponibles. Contacte al administrador.')
                return redirect('cart_detail')
        except Exception as e:
            messages.error(request, f'Error al obtener vendedor: {str(e)}')
            return redirect('cart_detail')
        
        if request.method == 'POST':
            # Crear la orden
            try:
                orden = OrdenCompraCliente.objects.create(
                    pedido_id=uuid.uuid4(),
                    cliente=cliente,
                    vendedor=vendedor,
                    estado=1,  # Pendiente
                    notas=request.POST.get('notas', ''),
                    creado_por=request.user
                )
                
                # Crear los items de la orden
                item_number = 1
                for item in cart:
                    articulo = item['articulo']
                    ItemOrdenCompraCliente.objects.create(
                        item_id=uuid.uuid4(),
                        pedido=orden,
                        nro_item=item_number,
                        articulo=articulo,
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio'],
                        creado_por=request.user
                    )
                    item_number += 1
                
                # Limpiar el carrito
                cart.clear()
                
                messages.success(request, f'¡Orden creada exitosamente! Tu número de orden es: {orden.nro_pedido}')
                return redirect('order_detail', pedido_id=orden.pedido_id)
                
            except Exception as e:
                messages.error(request, f'Error al procesar la orden: {str(e)}')
                return redirect('cart_detail')
        
        return render(request, 'core/cart/checkout.html', {
            'cart': cart,
            'cliente': cliente
        })
        
    except Exception as e:
        messages.error(request, f'Error en checkout: {str(e)}')
        return redirect('cart_detail')

@login_required
def order_detail(request, pedido_id):
    """Ver detalle de una orden"""
    try:
        orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
        
        # Verificar que la orden pertenece al usuario actual
        if orden.cliente.correo_electronico != request.user.email and not request.user.is_staff:
            messages.error(request, 'No tienes permiso para ver esta orden.')
            return redirect('dashboard')
        
        return render(request, 'core/cart/order_detail.html', {'orden': orden})
        
    except Exception as e:
        messages.error(request, f'Error al cargar orden: {str(e)}')
        return redirect('dashboard')