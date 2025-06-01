# core/forms.py
from django import forms
from .models import Articulo, GrupoArticulo, LineaArticulo, ListaPrecio
from pos_project.choices import EstadoEntidades

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codigo_articulo', 'codigo_barras', 'descripcion', 'presentacion', 
                 'grupo', 'linea', 'stock']
        widgets = {
            'codigo_articulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese código del artículo',
                'required': True
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de barras (opcional)'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del artículo',
                'required': True
            }),
            'presentacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Presentación (opcional)'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'linea': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1',
                'placeholder': '0'
            })
        }
        labels = {
            'codigo_articulo': 'Código del Artículo',
            'codigo_barras': 'Código de Barras',
            'descripcion': 'Descripción',
            'presentacion': 'Presentación',
            'grupo': 'Grupo',
            'linea': 'Línea',
            'stock': 'Stock Inicial'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo grupos activos
        self.fields['grupo'].queryset = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO)
        
        # Si hay una instancia (editando), filtrar líneas por grupo
        if self.instance.pk and self.instance.grupo:
            self.fields['linea'].queryset = LineaArticulo.objects.filter(
                grupo=self.instance.grupo, 
                estado=EstadoEntidades.ACTIVO
            )
        else:
            # Si no hay instancia o grupo, mostrar líneas vacías
            self.fields['linea'].queryset = LineaArticulo.objects.none()
        
        # Hacer campos requeridos más explícitos
        self.fields['codigo_articulo'].required = True
        self.fields['descripcion'].required = True
        self.fields['grupo'].required = True
        self.fields['linea'].required = True

    def clean_codigo_articulo(self):
        codigo = self.cleaned_data['codigo_articulo']
        
        # Verificar que el código no exista (excepto para la instancia actual)
        qs = Articulo.objects.filter(codigo_articulo=codigo)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise forms.ValidationError('Ya existe un artículo con este código.')
        
        return codigo

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

class ListaPrecioForm(forms.ModelForm):
    class Meta:
        model = ListaPrecio
        fields = ['precio_1', 'precio_2', 'precio_compra', 'precio_costo']
        widgets = {
            'precio_1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00',
                'required': True
            }),
            'precio_2': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'precio_costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            })
        }
        labels = {
            'precio_1': 'Precio de Venta 1',
            'precio_2': 'Precio de Venta 2',
            'precio_compra': 'Precio de Compra',
            'precio_costo': 'Precio de Costo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_1'].required = True

    def clean_precio_1(self):
        precio = self.cleaned_data['precio_1']
        if precio <= 0:
            raise forms.ValidationError('El precio de venta debe ser mayor a 0.')
        return precio

    def clean_precio_2(self):
        precio = self.cleaned_data.get('precio_2')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_precio_compra(self):
        precio = self.cleaned_data.get('precio_compra')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_precio_costo(self):
        precio = self.cleaned_data.get('precio_costo')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

class GrupoArticuloForm(forms.ModelForm):
    class Meta:
        model = GrupoArticulo
        fields = ['nombre_grupo']
        widgets = {
            'nombre_grupo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del grupo',
                'required': True
            })
        }
        labels = {
            'nombre_grupo': 'Nombre del Grupo'
        }

    def clean_nombre_grupo(self):
        nombre = self.cleaned_data['nombre_grupo']
        
        # Verificar que el nombre no exista (excepto para la instancia actual)
        qs = GrupoArticulo.objects.filter(nombre_grupo=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise forms.ValidationError('Ya existe un grupo con este nombre.')
        
        return nombre

class LineaArticuloForm(forms.ModelForm):
    class Meta:
        model = LineaArticulo
        fields = ['nombre_linea', 'grupo']
        widgets = {
            'nombre_linea': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la línea',
                'required': True
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'nombre_linea': 'Nombre de la Línea',
            'grupo': 'Grupo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo grupos activos
        self.fields['grupo'].queryset = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO)
        
        self.fields['nombre_linea'].required = True
        self.fields['grupo'].required = True

    def clean_nombre_linea(self):
        nombre = self.cleaned_data['nombre_linea']
        grupo = self.cleaned_data.get('grupo')
        
        if grupo:
            # Verificar que no exista otra línea con el mismo nombre en el mismo grupo
            qs = LineaArticulo.objects.filter(nombre_linea=nombre, grupo=grupo)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError('Ya existe una línea con este nombre en el grupo seleccionado.')
        
        return nombre