from django.db import models
from django.contrib.auth.models import AbstractUser
from pos_project.choices import EstadoEntidades, EstadoOrden
import uuid

# Modelo de Usuario personalizado
class Usuario(AbstractUser):
    usuario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = "usuarios"

# Modelos básicos del sistema
class TipoIdentificacion(models.Model):
    tipo_id = models.AutoField(primary_key=True)
    nombre_tipo_identificacion = models.CharField(max_length=100)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_tipo_identificacion
    
    class Meta:
        db_table = "tipos_identificacion"

class CanalCliente(models.Model):
    canal_id = models.AutoField(primary_key=True)
    nombre_canal = models.CharField(max_length=100)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_canal
    
    class Meta:
        db_table = "canales_cliente"

class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT)
    nro_documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    canal = models.ForeignKey(CanalCliente, on_delete=models.RESTRICT)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombres
    
    class Meta:
        db_table = "clientes"

class Vendedor(models.Model):
    vendedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=255)
    correo_electronico = models.EmailField()
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombres
    
    class Meta:
        db_table = "vendedores"

class GrupoArticulo(models.Model):
    grupo_id = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=100)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_grupo
    
    class Meta:
        db_table = "grupos_articulo"

class LineaArticulo(models.Model):
    linea_id = models.AutoField(primary_key=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE)
    nombre_linea = models.CharField(max_length=100)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_linea
    
    class Meta:
        db_table = "lineas_articulo"

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_articulo = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT)
    linea = models.ForeignKey(LineaArticulo, on_delete=models.RESTRICT)
    stock = models.IntegerField(default=0)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.descripcion
    
    @property
    def listaprecio(self):
        """Obtener el primer precio del artículo"""
        return self.precios.first()
    
    class Meta:
        db_table = "articulos"

class ListaPrecio(models.Model):
    precio_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='precios')
    precio_1 = models.DecimalField(max_digits=12, decimal_places=2)
    precio_2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "lista_precios"

# Modelos del carrito (que ya tienes)
class OrdenCompraCliente(models.Model):
    pedido_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nro_pedido = models.BigAutoField(unique=True, null=False, auto_created=True)
    fecha_pedido = models.DateField(auto_now_add=True, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.RESTRICT, null=False)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(choices=EstadoOrden, default=EstadoOrden.PENDIENTE)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def actualizar_total(self):
        """Actualiza el total de la orden basado en los items"""
        total = sum(item.total_item for item in self.items_orden_compra.all())
        self.importe = total
        self.save()

    def __str__(self):
        return f"Orden #{self.nro_pedido} - {self.cliente}"

    class Meta:
        db_table = "ordenes_compra_cliente"
        ordering = ["-fecha_creacion"]

class ItemOrdenCompraCliente(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(OrdenCompraCliente, on_delete=models.CASCADE, 
                              null=False, related_name='items_orden_compra')
    nro_item = models.PositiveIntegerField(default=1, null=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT, 
                                null=False, related_name='articulo_item_orden_compra')
    cantidad = models.PositiveIntegerField(null=False, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    total_item = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def save(self, *args, **kwargs):
        # Calcular el total del item
        self.total_item = self.cantidad * self.precio_unitario
        
        # Si no se ha establecido el precio unitario, tomarlo del artículo
        if self.precio_unitario == 0:
            try:
                lista_precio = self.articulo.listaprecio
                self.precio_unitario = lista_precio.precio_1
                self.total_item = self.cantidad * self.precio_unitario
            except:
                pass
        
        super().save(*args, **kwargs)
        
        # Actualizar el total de la orden
        self.pedido.actualizar_total()

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.descripcion}"

    class Meta:
        db_table = "items_ordenes_compra_cliente"