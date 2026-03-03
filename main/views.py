from django.shortcuts import render
from django.http import JsonResponse
import json


# Page view (HTML)
def api_form(request):
    return render(request, "api_form.html")


# API view (receives data)
def my_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        age = data.get("age")

        return JsonResponse({
            "message": f"Hello {name}, you are {age} years old!"
        })
        

def product_ui(request):
    return render(request, "product_ui.html")

def products_index(request):
    products = [
        {"id": 1, "name": "Product A", "price": 10.99},
        {"id": 2, "name": "Product B", "price": 19.99},
        {"id": 3, "name": "Product C", "price": 5.49},
    ]
    return JsonResponse(products, safe=False)


from rest_framework import viewsets
from .models import SmartBin
from .serializers import SmartBinSerializer

class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer

