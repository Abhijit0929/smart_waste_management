from django.contrib import admin
from .models import SmartBin, Pickup, WasteReport 

# Register your models here.

admin.site.register(SmartBin)
admin.site.register(Pickup)
admin.site.register(WasteReport)