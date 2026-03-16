from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#-------USER MODEL-------#

from django.db import models
from django.contrib.auth.models import User


# -------- SMART BIN MODEL -------- #
class SmartBin(models.Model):
    location = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    fill_level = models.IntegerField(default=0)  # 0–100%
    status = models.CharField(
        max_length=10,
        choices=[("empty", "Empty"), ("full", "Full")]
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location


# -------- PICKUP MODEL -------- #
class Pickup(models.Model):
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE)
    assigned_worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=15,
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed")
        ]
    )
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"Pickup for {self.bin.location}"


# -------- WASTE REPORT MODEL -------- #
class WasteReport(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    location = models.CharField(max_length=100)
    description = models.TextField()

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    status = models.CharField(
        max_length=10,
        choices=[("open","Open"),("resolved","Resolved")]
    )

    def __str__(self):
        return f"Report at {self.location}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    