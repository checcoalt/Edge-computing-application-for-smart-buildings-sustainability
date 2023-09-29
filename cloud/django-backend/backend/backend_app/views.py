from django.shortcuts import render
import datetime
from django.utils import timezone

# Create your views here.

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Libellium

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

def home_view(request):
    return render(request, 'html/home.html')

def temperature_view(request):
    return render(request, 'html/temperature.html')

def temperature_view_day(request):
    result_json = build_json_day("Temperature (°C)", "TC")

    return JsonResponse(result_json, safe=False)

def temperature_view_month(request):
    
    result_json = build_json_month("Temperature (°C)", "TC")

    return JsonResponse(result_json, safe=False)

def temperature_view_year(request):
    
    result_json = build_json_year("Temperature (°C)", "TC")

    return JsonResponse(result_json, safe=False)

def humidity_view(request):
    return render(request, 'html/humidity.html')

def humidity_view_day(request):
    
    result_json = build_json_day("Humidity (%)", "HUM")

    return JsonResponse(result_json, safe=False)

def humidity_view_month(request):
    
    result_json = build_json_month("Humidity (%)", "HUM")

    return JsonResponse(result_json, safe=False)

def humidity_view_year(request):
    
    result_json = build_json_year("Humidity (%)", "HUM")

    return JsonResponse(result_json, safe=False)

def co2_view(request):
    return render(request, 'html/co2.html')

def co2_view_day(request):
    
    result_json = build_json_day("CO2 (ppm)", "CO")

    return JsonResponse(result_json, safe=False)

def co2_view_month(request):
    
    result_json = build_json_month("CO2 (ppm)", "CO")

    return JsonResponse(result_json, safe=False)

def co2_view_year(request):
    
    result_json = build_json_year("CO2 (ppm)", "CO")

    return JsonResponse(result_json, safe=False)

def energy_view(request):
    return render(request, 'html/energy.html')



def build_json_day(label, parameter):
    # Assuming timestamp is your datetime field
    current_datetime = timezone.now()

    # Calculate the start of the 24-hour slot
    start_datetime = current_datetime - datetime.timedelta(hours=24)


    # Calculate the end of the 24-hour slot
    end_datetime = current_datetime
    print(end_datetime)
    measurements = Libellium.objects.filter(timestamp__range=(start_datetime, end_datetime))

    # Create metadata dictionary
    metadata = {
        "type": "line",
        "mainLabel": label
    }

    # Create data list
    data = []
    # Iterate through Libellium instances
    for instance in measurements:
        time = instance.timestamp.strftime("%Y-%m-%d %H:%M")  # Format timestamp as yyyy-mm-dd hh:mm
        # time = instance.timestamp.strftime("%H:%M")  # Format timestamp as hh:mm
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

def build_json_month(label, parameter):
   # Assuming timestamp is your datetime field
    current_datetime = timezone.now()

    # Calculate the end of the 30-day slot (which is the current date's end of day)
    end_datetime = datetime.datetime.combine(current_datetime, datetime.datetime.max.time())  # This is equivalent to datetime.datetime.combine(current_date, datetime.time.max)
    print(end_datetime)
    # Calculate the start of the 30-day slot
    start_datetime = end_datetime - datetime.timedelta(days=30)
    print(start_datetime)
    measurements = Libellium.objects.filter(timestamp__range=(start_datetime, end_datetime))
    # Create metadata dictionary
    metadata = {
        "type": "line",
        "mainLabel": label
    }

    # Create data list
    data = []
    # Iterate through Libellium instances
    for instance in measurements:
        time = instance.timestamp.strftime("%Y-%m-%d %H:%M")  # Format timestamp as yyyy-mm-dd hh:mm
        # time = instance.timestamp.strftime("%H:%M")  # Format timestamp as hh:mm
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

def build_json_year(label, parameter):
    # Assuming timestamp is your datetime field
    current_datetime = timezone.now()

    # Calculate the end of the 1-year slot (which is the current date's end of day)
    end_datetime = datetime.datetime.combine(current_datetime, datetime.datetime.max.time())

    # Calculate the start of the 1-year slot
    start_datetime = end_datetime - datetime.timedelta(days=365)

    measurements = Libellium.objects.filter(timestamp__range=(start_datetime, end_datetime))

    print(start_datetime)
    print(end_datetime)

    # Create metadata dictionary
    metadata = {
        "type": "line",
        "mainLabel": label
    }

    # Create data list
    data = []
    # Iterate through Libellium instances
    for instance in measurements:
        time = instance.timestamp.strftime("%Y-%m-%d %H:%M")  # Format timestamp as yyyy-mm-dd hh:mm
        # time = instance.timestamp.strftime("%H:%M")  # Format timestamp as hh:mm
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