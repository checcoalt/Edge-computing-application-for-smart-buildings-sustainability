from django.urls import path
from .views import display_json, list_json_data

urlpatterns = [
    path('display/', display_json, name='display_json'),
    path('list/', list_json_data, name='list_json_data'),
]