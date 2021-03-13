"""proyectots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from proyectots import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Inicio),
    path('congruencial/', views.Congruencial),
    path('congruencialr/', views.Congruencialr),
    path('congruencialm/', views.Congruencialm),
    path('congruencialmr/', views.Congruencialmr),
    path('lineaespera/', views.LineaEspera),
    path('lineaesperar/', views.LineaEsperar),
    path('montecarlo/', views.Montecarlo),
    path('montecarlor/', views.Montecarlor),
    path('grafico/', views.Grafico),
    path('graficor/', views.Graficor),
    path('exponencial/', views.Exponencial),
    path('exponencialr/', views.Exponencialr),
    path('index/', views.Inicio),
    path('simulacion/', views.Simulacion),

]
