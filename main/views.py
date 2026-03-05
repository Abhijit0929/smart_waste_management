from django.shortcuts import render
from django.http import JsonResponse
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SmartBin, Pickup, WasteReport
from .serializers import SmartBinSerializer, PickupSerializer, WasteReportSerializer



# Page view (HTML)
from rest_framework import viewsets
from .models import SmartBin
from .serializers import SmartBinSerializer



@api_view(['PATCH'])
def update_pickup_status(request, id):

    pickup = Pickup.objects.get(id=id)

    serializer = PickupSerializer(
        pickup,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET', 'POST'])
def bin_list_create(request):

    if request.method == "GET":
        bins = SmartBin.objects.all()
        serializer = SmartBinSerializer(bins, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = SmartBinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(['PATCH'])
def bin_update(request, id):

    bin = SmartBin.objects.get(id=id)

    serializer = SmartBinSerializer(
        bin,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET','POST'])
def pickup_list_create(request):

    if request.method == "GET":
        pickups = Pickup.objects.all()
        serializer = PickupSerializer(pickups, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PickupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
@api_view(['GET','POST'])
def report_list_create(request):

    if request.method == "GET":
        reports = WasteReport.objects.all()
        serializer = WasteReportSerializer(reports, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = WasteReportSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer


from django.shortcuts import render, redirect
from .models import SmartBin, WasteReport


def home(request):

    return render(request,"home.html")


def bins_view(request):

    bins = SmartBin.objects.all()

    return render(request,"bins.html",{"bins":bins})


def report_waste(request):

    if request.method == "POST":

        location = request.POST.get("location")
        description = request.POST.get("description")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        WasteReport.objects.create(
            location=location,
            description=description,
            latitude=latitude,
            longitude=longitude,
            status="open",
            user=request.user
        )

        return redirect("/reports/")

    return render(request,"report.html")

def reports_view(request):

    reports = WasteReport.objects.all()

    return render(request,"reports.html",{"reports":reports})


# Pickups page view

from .models import Pickup

def pickups_view(request):

    pickups = Pickup.objects.all()

    return render(request, "pickups.html", {"pickups": pickups})



def update_pickup(request, id):

    pickup = Pickup.objects.get(id=id)

    if pickup.status == "pending":
        pickup.status = "in_progress"

    elif pickup.status == "in_progress":
        pickup.status = "completed"

    pickup.save()

    return redirect("/pickups/")