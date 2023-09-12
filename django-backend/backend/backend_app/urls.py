from django.urls import path
from .views import display_json

urlpatterns = [
    path('display/', display_json, name='display_json'),
]