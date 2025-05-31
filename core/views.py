from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import (
    Articulo, GrupoArticulo, LineaArticulo, ListaPrecio,
    Cliente, Vendedor, OrdenCompraCliente, ItemOrdenCompraCliente,
    TipoIdentificacion, CanalCliente
)
from pos_project.choices import EstadoOrden, EstadoEntidades
from .cart import Cart
import uuid

@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    context = {
        'total_articulos': Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).count(),
        'total_clientes': Cliente.objects.filter(estado=EstadoEntidades.ACTIVO).count(),
        'ordenes_pendientes': OrdenCompraCliente.objects.filter(estado=EstadoOrden.PENDIENTE).count(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def articulos_list(request):
    """Vista para listar artículos con paginación"""
    articulos_list = Articulo.objects.filter(estado=EstadoEntidades.ACTIVO).select_related('grupo', 'linea')
    
    # Filtros
    q = request.GET.get('q')
    if q:
        articulos_list = articulos_list.filter(descripcion__icontains=q)
    
    # Paginación
    paginator = Paginator(articulos_list, 15)  # 15 artículos por página
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)
    
    context = {
        'articulos': articulos,
        'search_query': q,
    }
    return render(request, 'core/articulos/list.html', context)

@login_required
def articulo_detail(request, articulo_id):
    """Vista para ver el detalle de un artículo"""
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
        recent_uuids = [uuid.UUID(id_str) for id_str in viewed_products[1:6]]  # Excluir el actual
        if recent_uuids:
            recent_products = Articulo.objects.filter(articulo_id__in=recent_uuids)
    
    context = {
        'articulo': articulo,
        'recent_products': recent_products,
    }
    return render(request, 'core/articulos/detail.html', context)

# API para obtener líneas por grupo
def lineas_por_grupo(request, grupo_id):
    """API para obtener líneas de artículo por grupo"""
    lineas = LineaArticulo.objects.filter(
        grupo_id=grupo_id, 
        estado=EstadoEntidades.ACTIVO
    ).values('linea_id', 'nombre_linea')
    return JsonResponse(list(lineas), safe=False)

# VISTAS DEL CARRITO DE COMPRAS

@require_POST
def cart_add(request, articulo_id):
    """Añadir artículo al carrito"""
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    cantidad = int(request.POST.get('cantidad', 1))
    update = request.POST.get('update')
    
    cart.add(articulo=articulo, cantidad=cantidad, update_cantidad=update)
    messages.success(request, f'"{articulo.descripcion}" añadido al carrito.')
    
    return redirect('cart_detail')

def cart_remove(request, articulo_id):
    """Eliminar artículo del carrito"""
    cart = Cart(request)
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    cart.remove(articulo)
    messages.info(request, f'"{articulo.descripcion}" eliminado del carrito.')
    
    return redirect('cart_detail')

def cart_detail(request):
    """Ver detalle del carrito"""
    cart = Cart(request)
    return render(request, 'core/cart/detail.html', {'cart': cart})

def cart_clear(request):
    """Vaciar el carrito"""
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Carrito vaciado correctamente.')
    
    return redirect('cart_detail')

@login_required
def checkout(request):
    """Finalizar compra"""
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
            
            # Crear cliente con datos básicos del usuario
            cliente = Cliente.objects.create(
                cliente_id=uuid.uuid4(),
                tipo_identificacion=tipo_id,
                nro_documento=request.user.username[:11],
                nombres=request.user.full_name or request.user.username,
                correo_electronico=request.user.email,
                canal=canal,
                estado=EstadoEntidades.ACTIVO
            )
        except:
            messages.error(request, 'Error al procesar el cliente. Contacte al administrador.')
            return redirect('cart_detail')
    
    # Obtener vendedor predeterminado para la orden
    try:
        vendedor = Vendedor.objects.first()
    except:
        messages.error(request, 'No hay vendedores disponibles. Contacte al administrador.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        # Crear la orden
        try:
            orden = OrdenCompraCliente.objects.create(
                pedido_id=uuid.uuid4(),
                cliente=cliente,
                vendedor=vendedor,
                estado=EstadoOrden.PENDIENTE,
                notas=request.POST.get('notas', ''),
                creado_por=request.user
            )
            
            # Crear los items de la orden
            for item in cart:
                articulo = item['articulo']
                ItemOrdenCompraCliente.objects.create(
                    item_id=uuid.uuid4(),
                    pedido=orden,
                    nro_item=1,
                    articulo=articulo,
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    creado_por=request.user
                )
            
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

@login_required
def order_detail(request, pedido_id):
    """Ver detalle de una orden"""
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id)
    
    # Verificar que la orden pertenece al usuario actual
    if orden.cliente.correo_electronico != request.user.email and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta orden.')
        return redirect('dashboard')
    
    return render(request, 'core/cart/order_detail.html', {'orden': orden})