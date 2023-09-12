from django.shortcuts import render

# Create your views here.

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JSONData

@csrf_exempt # This decorator is used to exempt the csrf token check
def display_json(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            # Save JSON data to the database
            JSONData.objects.create(data=json_data)
            return render(request, 'display.html', {'json_data': json_data})
        except json.JSONDecodeError as e:
            return render(request, 'error.html', {'error_message': 'Invalid JSON format'})
    else:
        return render(request, 'error.html', {'error_message': 'Method not allowed'})
    
def list_json_data(request):
    json_data_list = JSONData.objects.all()
    return render(request, 'list.html', {'json_data_list': json_data_list})