"""
URL configuration for hotelmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from habitaciones.views import dashboard_recepcion
from reservas.views import seleccionar_huesped, crear_huesped_y_reserva
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_recepcion, name='dashboard_recepcion'),
    path('reservar/<int:habitacion_id>/', seleccionar_huesped, name='seleccionar_huesped'),
    path('reservar/<int:habitacion_id>/crear/', crear_huesped_y_reserva, name='crear_huesped_y_reserva'),
]
