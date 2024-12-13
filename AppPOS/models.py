from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()  # Este es el campo que mantiene el inventario

    def __str__(self):
        return self.nombre

    def actualizar_stock(self, cantidad_vendida):
        """Método para actualizar el stock después de una venta."""
        if self.cantidad >= cantidad_vendida:
            self.cantidad -= cantidad_vendida
            self.save()
        else:
            raise ValueError("No hay suficiente stock para la venta")

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    cliente = models.CharField(max_length=100)
    direccion_cliente = models.CharField(max_length=255)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta de {self.producto.nombre} a {self.cliente}"

    def registrar_venta(self):
        """Método para registrar la venta y actualizar el stock del producto."""
        # Actualizamos el inventario del producto
        self.producto.actualizar_stock(self.cantidad)
        self.save()

class RegistroVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro {self.id} - Venta {self.venta.id}"

# Signal para actualizar el inventario cuando se guarda una venta
@receiver(post_save, sender=Venta)
def actualizar_inventario(sender, instance, created, **kwargs):
    """Después de registrar una venta, se actualiza el stock."""
    if created:
        # Aquí no es necesario llamar a registrar_venta, ya que se hace dentro del modelo
        # instance.registrar_venta()
        pass  # Se puede dejar vacío o eliminar esta señal si no es estrictamente necesaria.
