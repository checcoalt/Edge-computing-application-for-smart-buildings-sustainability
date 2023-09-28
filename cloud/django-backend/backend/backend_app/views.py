from django.shortcuts import render
import datetime

# Create your views here.

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Libellium

@csrf_exempt # This decorator is used to exempt the csrf token check

def home_view(request):
    return render(request, 'html/home.html')

def temperature_view(request):
    return render(request, 'html/temperature.html')

def temperature_view_day(request):
    
    result_json = build_json("Temperature (°C)", "TC")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def temperature_view_month(request):
    
    result_json = build_json("Temperature (°C)", "TC")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def temperature_view_year(request):
    
    result_json = build_json("Temperature (°C)", "TC")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def humidity_view(request):
    return render(request, 'html/humidity.html')

def humidity_view_day(request):
    
    result_json = build_json("humidity (°C)", "HUM")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def humidity_view_month(request):
    
    result_json = build_json("humidity (°C)", "HUM")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def humidity_view_year(request):
    
    result_json = build_json("humidity (°C)", "HUM")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def co2_view(request):
    return render(request, 'html/co2.html')

def co2_view_day(request):
    
    result_json = build_json("co2 (°C)", "CO")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def co2_view_month(request):
    
    result_json = build_json("co2 (°C)", "CO")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def co2_view_year(request):
    
    result_json = build_json("co2 (°C)", "CO")

    print(result_json)

    return JsonResponse(result_json, safe=False)

def energy_view(request):
    return render(request, 'html/energy.html')



def build_json(label, parameter):
    measurements = Libellium.objects.all()
    
    # Create metadata dictionary
    metadata = {
        "type": "line",
        "mainLabel": label
    }

    # Create data list
    data = []
    # Iterate through Libellium instances
    for instance in measurements:
        time = instance.timestamp.strftime("%H:%M")  # Format timestamp as hh:mm
        if parameter=="TC": value = instance.TC  # Assuming TC is temperature in °C
        if parameter=="HUM": value = instance.HUM
        if parameter=="CO": value = instance.CO

        # Create data point dictionary
        data_point = {"time": time, "value": value}

        # Add data point to data list
        data.append(data_point)

    result = {
    "metadata": metadata,
    "data": data
    }

    # Convert the dictionary to a JSON string
    result_json = json.dumps(result)
    return result_json