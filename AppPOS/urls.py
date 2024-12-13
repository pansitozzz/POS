from django.urls import path, include  # Asegúrate de incluir 'include' aquí
from rest_framework import routers
from . import views

# Crea el router y registra las vistas de la API
router = routers.DefaultRouter()
router.register('producto', views.ProductoViewSet)
router.register('venta', views.VentaViewSet)
router.register('registroventas', views.RegistroVentaViewSet)

# Define las rutas en 'urlpatterns'
urlpatterns = [
    path('registrodeventas/', views.registrar_venta, name='registroventas'),  # Vista para registrar ventas
    path('ventas/', views.ventas, name='ventas'),  # Vista para ver las ventas registradas
    path('', include(router.urls)),  # Incluir las rutas de la API sin el prefijo 'api/'
]