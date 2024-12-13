from rest_framework import serializers
from .models import Venta, Producto, RegistroVenta

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields='__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields='__all__'

class RegistroDeVentasSerializer(serializers.Serializer):
    cliente = serializers.CharField(max_length=100)
    producto = serializers.CharField(max_length=100)
    cantidad = serializers.IntegerField()
    precio = serializers.FloatField()
    fecha = serializers.DateField()

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value