from django.urls import path,include
from . import views

from django.contrib import admin



urlpatterns = [
    
       # ---------- HTML UI ----------
    path("", views.home, name="home"),
    path("bins/", views.bins_view, name="bins"),
    path("report/", views.report_waste, name="report"),
    path("reports/", views.reports_view, name="reports"),


    # ---------- API ----------
    path("api/bins/", views.bin_list_create),
    path("api/bins/<int:id>/", views.bin_update),

    path("api/pickups/", views.pickup_list_create),
    path("api/pickups/<int:id>/", views.update_pickup_status),

    path("api/reports/", views.report_list_create),
    path("pickups/", views.pickups_view),
    path("pickup/update/<int:id>/", views.update_pickup),

]

