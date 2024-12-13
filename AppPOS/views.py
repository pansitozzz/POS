from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto, Venta, RegistroVenta
from .forms import ProductoForm, VentaForm
from .serializer import ProductoSerializer, VentaSerializer, RegistroDeVentasSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegistroDeVentasSerializer


# Vista de inicio
def inicio(request):
    return render(request, 'AppPOS/inicio.html')

# Vista para mostrar productos
def productos(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'AppPOS/productos.html', {'productos': productos})

# Vista para agregar un nuevo producto
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el producto
            return redirect('productos')  # Redirigir a la lista de productos
    else:
        form = ProductoForm()

    return render(request, 'AppPOS/agregar_producto.html', {'form': form})

# Vista para editar un producto existente
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('productos')  # Redirigir a la lista de productos
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'AppPOS/editar_producto.html', {'form': form})

# Vista para eliminar un producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()  # Eliminar el producto
        return redirect('productos')  # Redirigir a la lista de productos
    return render(request, 'AppPOS/eliminar_producto.html', {'producto': producto})

# Vista para registrar una venta
def registrar_venta(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            cliente = form.cleaned_data['cliente']
            direccion_cliente = form.cleaned_data['direccion_cliente']
            precio_total = float(request.POST.get('precio_total'))  # Obtener el precio total desde el formulario

            try:
                # Crear la venta
                venta = Venta.objects.create(
                    cliente=cliente,
                    direccion_cliente=direccion_cliente,
                    producto=producto,
                    cantidad=cantidad,
                    precio_total=precio_total
                )

                # Actualizar el stock del producto después de registrar la venta
                producto.cantidad -= cantidad
                producto.save()

                # Redirigir a la lista de ventas o la página principal de ventas
                return redirect('ventas')  # Asegúrate de tener definida esta ruta correctamente
            except Exception as e:
                # Manejar cualquier excepción y devolver un mensaje de error
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # Si el formulario no es válido, devolver un error en la respuesta
            return JsonResponse({'error': 'Formulario no válido'}, status=400)

    else:
        # Si el método no es POST, devolver el formulario en la vista
        form = VentaForm()
        return render(request, 'AppPOS/registrar_venta.html', {'productos': productos, 'form': form})

# Vista para mostrar todas las ventas registradas
def ventas(request):
    ventas_registradas = Venta.objects.all()  # Obtener todas las ventas
    return render(request, 'AppPOS/historial_ventas.html', {'ventas': ventas_registradas})

# ViewSet para productos (API)
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# ViewSet para ventas (API)
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

# ViewSet para registro de ventas (API)
class RegistroVentaViewSet(viewsets.ModelViewSet):
    queryset = RegistroVenta.objects.all()  # Conjunto de datos del modelo
    serializer_class = RegistroDeVentasSerializer  # Serializador para este modelo