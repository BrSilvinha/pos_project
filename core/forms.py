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
                'placeholder': 'Ingrese código del artículo'
            }),
            'codigo_barras': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de barras (opcional)'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del artículo'
            }),
            'presentacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Presentación (opcional)'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'linea': forms.Select(attrs={
                'class': 'form-select'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ CORREGIDO: Usar EstadoEntidades.ACTIVO en lugar de 'A'
        self.fields['grupo'].queryset = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO)
        
        # Si hay una instancia, filtrar líneas por grupo
        if self.instance.pk:
            self.fields['linea'].queryset = LineaArticulo.objects.filter(
                grupo=self.instance.grupo, estado=EstadoEntidades.ACTIVO
            )
        else:
            self.fields['linea'].queryset = LineaArticulo.objects.none()

class ListaPrecioForm(forms.ModelForm):
    class Meta:
        model = ListaPrecio
        fields = ['precio_1', 'precio_2', 'precio_compra', 'precio_costo']
        widgets = {
            'precio_1': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
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

class GrupoArticuloForm(forms.ModelForm):
    class Meta:
        model = GrupoArticulo
        fields = ['nombre_grupo']
        widgets = {
            'nombre_grupo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del grupo'
            })
        }

class LineaArticuloForm(forms.ModelForm):
    class Meta:
        model = LineaArticulo
        fields = ['nombre_linea', 'grupo']
        widgets = {
            'nombre_linea': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la línea'
            }),
            'grupo': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ CORREGIDO: Usar EstadoEntidades.ACTIVO en lugar de 'A'
        self.fields['grupo'].queryset = GrupoArticulo.objects.filter(estado=EstadoEntidades.ACTIVO)