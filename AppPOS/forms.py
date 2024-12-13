from django import forms
from .models import Producto, Venta
from django.shortcuts import render, redirect
from .models import Producto
from django.http import JsonResponse

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'cantidad', 'descripcion']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'cliente', 'direccion_cliente', 'precio_total']

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        producto = self.cleaned_data['producto']
        if cantidad > producto.cantidad:
            raise forms.ValidationError("La cantidad solicitada excede el inventario disponible.")
        return cantidad

def registrar_venta(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            nombre_cliente = form.cleaned_data['cliente']
            direccion_cliente = form.cleaned_data['direccion_cliente']

            # Calcular el precio total si no se pasa en el formulario
            precio_total = producto.precio * cantidad

            try:
                # Crear la venta directamente
                Venta.objects.create(
                    cliente=nombre_cliente,
                    direccion_cliente=direccion_cliente,
                    producto=producto,
                    cantidad=cantidad,
                    precio_total=precio_total
                )

                # Actualizar el stock del producto después de registrar la venta
                producto.cantidad -= cantidad
                producto.save()

                # Redirigir a la lista de ventas o la página principal de ventas
                return redirect('ventas')  # Asegúrate de tener esta ruta definida correctamente
            except Exception as e:
                # Manejar cualquier excepción y devolver un mensaje de error
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # Si el formulario no es válido, devolver un error en la respuesta con los detalles del error
            return JsonResponse({'error': form.errors}, status=400)
    else:
        # Si el método no es POST, devolver el formulario en la vista
        form = VentaForm()
        return render(request, 'AppPOS/registrar_venta.html', {'productos': productos, 'form': form})