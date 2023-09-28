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
    measurements = Libellium.objects.all()

    for instance in measurements:
        print(instance.timestamp)
    # Assuming timestamp is your datetime field
    current_date = timezone.now().date()
    print(current_date)

    # Get the start of the current day
    start_datetime = datetime.datetime.combine(current_date, datetime.time.min, tzinfo=timezone.utc)
    print(start_datetime)

    # Get the end of the current day
    end_datetime = datetime.datetime.combine(current_date, datetime.time.max, tzinfo=timezone.utc)
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
    current_year = timezone.now().year
    current_month = timezone.now().month

    # Get the first day of the current month
    start_date = datetime.datetime(year=current_year, month=current_month, day=1, tzinfo=timezone.utc)

    # Get the last day of the current month
    if current_month == 12:
        end_date = datetime.datetime(year=current_year + 1, month=1, day=1, tzinfo=timezone.utc) - datetime.timedelta(seconds=1)
    else:
        end_date = datetime.datetime(year=current_year, month=current_month + 1, day=1, tzinfo=timezone.utc) - datetime.timedelta(seconds=1)

    measurements = Libellium.objects.filter(timestamp__range=(start_date, end_date))
    
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
    current_year = timezone.now().year
    start_date = datetime.datetime(year=current_year, month=1, day=1, tzinfo=timezone.utc)
    end_date = datetime.datetime(year=current_year, month=12, day=31, hour=23, minute=59, second=59, tzinfo=timezone.utc)

    measurements = Libellium.objects.filter(timestamp__range=(start_date, end_date))
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