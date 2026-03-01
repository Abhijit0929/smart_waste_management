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
        
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
def product_ui(request):
    return render(request, "product_ui.html")

