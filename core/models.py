from django.db import models
from django.contrib.auth import get_user_model
from pos_project.choices import ESTADO_CHOICES

User = get_user_model()

class GrupoArticulo(models.Model):
    grupo_id = models.AutoField(primary_key=True)
    nombre_grupo = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'grupo_articulo'
        verbose_name = 'Grupo de Artículo'
        verbose_name_plural = 'Grupos de Artículos'

    def __str__(self):
        return self.nombre_grupo

class LineaArticulo(models.Model):
    linea_id = models.AutoField(primary_key=True)
    nombre_linea = models.CharField(max_length=100)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'linea_articulo'
        verbose_name = 'Línea de Artículo'
        verbose_name_plural = 'Líneas de Artículos'
        unique_together = ['nombre_linea', 'grupo']

    def __str__(self):
        return f"{self.nombre_linea} - {self.grupo.nombre_grupo}"

class Articulo(models.Model):
    articulo_id = models.AutoField(primary_key=True)
    codigo_articulo = models.CharField(max_length=50, unique=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200)
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE)
    linea = models.ForeignKey(LineaArticulo, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'articulo'
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

    def __str__(self):
        return f"{self.codigo_articulo} - {self.descripcion}"

class ListaPrecio(models.Model):
    precio_id = models.AutoField(primary_key=True)
    articulo = models.OneToOneField(Articulo, on_delete=models.CASCADE, related_name='precios')
    precio_1 = models.DecimalField(max_digits=10, decimal_places=2)
    precio_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lista_precio'
        verbose_name = 'Lista de Precio'
        verbose_name_plural = 'Listas de Precios'

    def __str__(self):
        return f"Precios - {self.articulo.descripcion}"