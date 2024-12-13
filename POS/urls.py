# urls.py principal del proyecto
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from AppPOS import views

urlpatterns = [
    # Rutas específicas de AppPOS
    path('', views.inicio, name='inicio'),  # Página de inicio
    path('productos/', views.productos, name='productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('admin/', admin.site.urls),  # Panel de administración
    path('docs/', include_docs_urls(title='API Documentation')),  # Documentación de la API
    path('api/', include('AppPOS.urls')),  # Incluir todas las rutas de la API desde AppPOS
]