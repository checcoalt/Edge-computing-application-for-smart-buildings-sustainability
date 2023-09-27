from django.shortcuts import render
import datetime

# Create your views here.

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JSONData, Libellium

@csrf_exempt # This decorator is used to exempt the csrf token check
def display_json(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            # Save JSON data to the database
            # JSONData.objects.create(data=json_data)

            # Convert the date and time to a datetime object
            datetime_str = f"{json_data['metadata']['date']}T{json_data['metadata']['time']}"
            formatted_datetime = datetime.datetime.fromisoformat(datetime_str)

            # Libellium creation
            lib = Libellium(timestamp=formatted_datetime,
                            CO = json_data['data']['CO']['value'],
                            O3 = json_data['data']['O3']['value'],
                            TC = json_data['data']['TC']['value'],
                            HUM = json_data['data']['HUM']['value'],
                            PRES = json_data['data']['PRES']['value'])
            
            # Save to database
            lib.save()
        
            return render(request, 'display.html', {'json_data': json_data})
        except json.JSONDecodeError as e:
            return render(request, 'error.html', {'error_message': 'Invalid JSON format'})
    else:
        return render(request, 'error.html', {'error_message': 'Method not allowed'})
    
def list_json_data(request):
    json_data_list = JSONData.objects.all()
    lib_list = Libellium.objects.all()
    return render(request, 'list.html', {'json_data_list': lib_list})

def home_view(request):
    return render(request, 'html/home.html')

def temperature_view(request):
    return render(request, 'html/temperature.html')

def humidity_view(request):
    return render(request, 'html/humidity.html')

def co2_view(request):
    return render(request, 'html/co2.html')

def energy_view(request):
    return render(request, 'html/energy.html')