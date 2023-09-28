"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from backend_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),

    path('display_json/', display_json, name='display_json'),

    path('temperature/', temperature_view, name='temperature'),
    path('temperature/day/', temperature_view_day, name='temperature_day'),
    path('temperature/month/', temperature_view_month, name='temperature_month'),
    path('temperature/year/', temperature_view_year, name='temperature_year'),

    path('humidity/', humidity_view, name='humidity'),
    path('humidity/day/', humidity_view_day, name='humidity_day'),
    path('humidity/month/', humidity_view_month, name='humidity_month'),
    path('humidity/year/', humidity_view_year, name='humidity_year'),

    path('co2/', co2_view, name='co2'),
    path('co2/day/', co2_view_day, name='co2_day'),
    path('co2/month/', co2_view_month, name='co2_month'),
    path('co2/year/', co2_view_year, name='co2_year'),

    path('energy/', energy_view, name='energy'),
]
