from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Articulo, GrupoArticulo, LineaArticulo, ListaPrecio
from .forms import ArticuloForm, ListaPrecioForm

User = get_user_model()

@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas básicas
    total_articulos = Articulo.objects.filter(estado='activo').count()
    ventas_hoy = 0  # Por implementar cuando tengamos el módulo de ventas
    total_usuarios = User.objects.filter(is_active=True).count()
    bajo_stock = Articulo.objects.filter(stock__lt=10, estado='activo').count()
    
    context = {
        'total_articulos': total_articulos,
        'ventas_hoy': ventas_hoy,
        'total_usuarios': total_usuarios,
        'bajo_stock': bajo_stock,
    }
    return render(request, 'core/index.html', context)

@login_required
def articulos_list(request):
    """Lista de artículos con búsqueda y paginación"""
    articulos = Articulo.objects.filter(estado='activo').select_related('grupo', 'linea')
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        articulos = articulos.filter(
            Q(descripcion__icontains=query) |
            Q(codigo_articulo__icontains=query) |
            Q(codigo_barras__icontains=query)
        )
    
    # Filtro de bajo stock
    stock_filter = request.GET.get('stock')
    if stock_filter == 'bajo':
        articulos = articulos.filter(stock__lt=10)
    
    # Paginación
    paginator = Paginator(articulos, 10)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)
    
    return render(request, 'core/articulos/list.html', {'articulos': articulos})

@login_required
def articulo_create(request):
    """Crear nuevo artículo"""
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        precio_form = ListaPrecioForm(request.POST)
        
        if form.is_valid() and precio_form.is_valid():
            articulo = form.save(commit=False)
            articulo.usuario_creacion = request.user
            articulo.save()
            
            precio = precio_form.save(commit=False)
            precio.articulo = articulo
            precio.save()
            
            messages.success(request, 'Artículo creado exitosamente.')
            return redirect('articulos_list')
    else:
        form = ArticuloForm()
        precio_form = ListaPrecioForm()
    
    return render(request, 'core/articulos/form.html', {
        'form': form,
        'precio_form': precio_form
    })

@login_required
def articulo_detail(request, pk):
    """Detalle de un artículo"""
    articulo = get_object_or_404(Articulo, pk=pk)
    return render(request, 'core/articulos/detail.html', {'articulo': articulo})

@login_required
def articulo_edit(request, pk):
    """Editar artículo existente"""
    articulo = get_object_or_404(Articulo, pk=pk)
    precio, created = ListaPrecio.objects.get_or_create(articulo=articulo)
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=precio)
        
        if form.is_valid() and precio_form.is_valid():
            form.save()
            precio_form.save()
            messages.success(request, 'Artículo actualizado exitosamente.')
            return redirect('articulos_list')
    else:
        form = ArticuloForm(instance=articulo)
        precio_form = ListaPrecioForm(instance=precio)
    
    return render(request, 'core/articulos/form.html', {
        'form': form,
        'precio_form': precio_form
    })

@login_required
def articulo_delete(request, pk):
    """Eliminar artículo (cambiar estado a inactivo)"""
    articulo = get_object_or_404(Articulo, pk=pk)
    
    if request.method == 'POST':
        articulo.estado = 'inactivo'
        articulo.save()
        messages.success(request, 'Artículo eliminado exitosamente.')
        return redirect('articulos_list')
    
    return render(request, 'core/articulos/delete.html', {'articulo': articulo})

@login_required
def lineas_por_grupo(request, grupo_id):
    """API endpoint para obtener líneas por grupo (AJAX)"""
    lineas = LineaArticulo.objects.filter(
        grupo_id=grupo_id, 
        estado='activo'
    ).values('linea_id', 'nombre_linea')
    
    return JsonResponse([
        {'id': linea['linea_id'], 'nombre': linea['nombre_linea']} 
        for linea in lineas
    ], safe=False)