from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SmartBin, Pickup, WasteReport, Feedback, Notification, UserProfile
from .serializers import SmartBinSerializer, PickupSerializer, WasteReportSerializer

from rest_framework import viewsets


# ════════════════════════════════════════════════
#  AUTH VIEWS
# ════════════════════════════════════════════════


#-------------------------------#
# LOGIN ADMIN USERNAME AND PASS : admin/PASSWORD@1234
#-------------------------------#

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username    = request.POST.get("username", "").strip()
        email       = request.POST.get("email", "").strip()
        password1   = request.POST.get("password1", "")
        password2   = request.POST.get("password2", "")

        error = None
        if not username or not password1:
            error = "Username and password are required."
        elif password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "That username is already taken."
        elif len(password1) < 6:
            error = "Password must be at least 6 characters."

        if error:
            return render(request, "register.html", {"error": error})

        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.get_or_create(user=user)
        login(request, user)
        messages.success(request, f"Welcome, {username}! Your account has been created.")
        return redirect("/")

    return render(request, "register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


def admin_login_view(request):
    """Dedicated login page for admin/staff users only."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/admin-dashboard/")
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect("/admin-dashboard/")
            else:
                return render(request, "admin_login.html", {
                    "error": "Access denied. This portal is for staff only."
                })
        else:
            return render(request, "admin_login.html", {
                "error": "Invalid username or password."
            })

    return render(request, "admin_login.html")


# ════════════════════════════════════════════════
#  API VIEWS
# ════════════════════════════════════════════════

@api_view(['PATCH'])
def update_pickup_status(request, id):
    pickup = Pickup.objects.get(id=id)
    serializer = PickupSerializer(pickup, data=request.data, partial=True)
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
    serializer = SmartBinSerializer(bin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'POST'])
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


@api_view(['GET', 'POST'])
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


# ════════════════════════════════════════════════
#  PAGE VIEWS
# ════════════════════════════════════════════════

def home(request):
    return render(request, "home.html")


def bins_view(request):
    bins = SmartBin.objects.all()
    return render(request, "bins.html", {"bins": bins})


def report_waste(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/report/")

    if request.method == "POST":
        location    = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        image       = request.FILES.get("image")

        raw_lat = request.POST.get("latitude", "").strip()
        raw_lon = request.POST.get("longitude", "").strip()
        latitude  = float(raw_lat) if raw_lat else None
        longitude = float(raw_lon) if raw_lon else None

        if not location or not description:
            return render(request, "report.html", {
                "error": "Please fill in the location and description before submitting."
            })

        WasteReport.objects.create(
            location=location,
            description=description,
            latitude=latitude,
            longitude=longitude,
            status="open",
            user=request.user,
            image=image,
        )

        # Notify admins about new report
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"📢 New garbage report filed at '{location}' by {request.user.username}."
            )

        return redirect("/reports/")

    return render(request, "report.html")


def reports_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/reports/")

    if request.user.is_staff:
        reports = WasteReport.objects.all().order_by("-id")
    else:
        reports = WasteReport.objects.filter(user=request.user).order_by("-id")

    return render(request, "reports.html", {"reports": reports})


def pickups_view(request):
    if not request.user.is_staff:
        return HttpResponse(status=403)
    pickups = Pickup.objects.all()
    return render(request, "admin_pickups.html", {"pickups": pickups})


def update_pickup(request, id):
    if not request.user.is_staff:
        return redirect("/dashboard/")

    pickup = Pickup.objects.get(id=id)

    if pickup.status == "pending":
        pickup.status = "in_progress"
    elif pickup.status == "in_progress":
        pickup.status = "completed"

    pickup.save()
    return redirect("/admin-dashboard/pickups/")


def city_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/dashboard/")

    bins    = SmartBin.objects.all()
    reports = WasteReport.objects.all()
    pickups = Pickup.objects.all()

    context = {
        "bins": bins,
        "reports": reports,
        "pickups": pickups,
    }

    return render(request, "dashboard.html", context)


def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")

    from django.db.models import Avg

    total_bins      = SmartBin.objects.count()
    full_bins       = SmartBin.objects.filter(status="full").count()
    pending_pickups = Pickup.objects.filter(status="pending").count()
    reports         = WasteReport.objects.count()
    workers         = User.objects.count()
    avg_fill        = SmartBin.objects.aggregate(avg=Avg("fill_level"))["avg"] or 0

    # ── AI Prediction Logic ──────────────────────────────────────────────────
    all_bins = SmartBin.objects.all()

    # Urgency buckets
    critical_bins = [b for b in all_bins if b.fill_level >= 85]   # needs pickup now
    warning_bins  = [b for b in all_bins if 60 <= b.fill_level < 85]  # fill soon
    healthy_bins  = [b for b in all_bins if b.fill_level < 60]

    # System health score (0–100, higher = better)
    if total_bins > 0:
        health_score = max(0, round(100 - (avg_fill * 0.7) - (len(critical_bins) / total_bins * 30)))
    else:
        health_score = 100

    # Estimated hours to full (simplified: assume 5% fill/hour rate)
    fill_rate_per_hour = 5
    bins_eta = []
    for b in all_bins:
        if b.fill_level < 100:
            hours = round((100 - b.fill_level) / fill_rate_per_hour, 1)
            bins_eta.append({"location": b.location, "fill_level": b.fill_level, "eta_hours": hours})
    bins_eta.sort(key=lambda x: x["eta_hours"])
    urgent_eta_bins = bins_eta[:5]   # top-5 bins closest to full

    # Overall prediction message
    if len(critical_bins) >= 3:
        ai_status = "critical"
        ai_message = f"{len(critical_bins)} bins require immediate collection. Dispatch teams now."
    elif len(critical_bins) >= 1:
        ai_status = "warning"
        ai_message = f"{len(critical_bins)} bin(s) critical + {len(warning_bins)} nearing capacity."
    elif len(warning_bins) >= 2:
        ai_status = "warning"
        ai_message = f"{len(warning_bins)} bins are nearing capacity. Schedule pickups soon."
    else:
        ai_status = "good"
        ai_message = "All bins are within safe fill levels. System is operating normally."

    context = {
        "total_bins":       total_bins,
        "full_bins":        full_bins,
        "pending_pickups":  pending_pickups,
        "reports":          reports,
        "workers":          workers,
        "avg_fill_level":   round(avg_fill),
        # AI Prediction context
        "ai_status":        ai_status,
        "ai_message":       ai_message,
        "health_score":     health_score,
        "critical_bins":    len(critical_bins),
        "warning_bins":     len(warning_bins),
        "healthy_bins":     len(healthy_bins),
        "urgent_eta_bins":  urgent_eta_bins,
    }

    return render(request, "admin_dashboard.html", context)


def admin_bins(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")
    bins = SmartBin.objects.all()
    return render(request, "admin_bins.html", {"bins": bins})


def admin_reports(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")
    reports       = WasteReport.objects.all().order_by("-id")
    open_count     = reports.filter(status="open").count()
    resolved_count = reports.filter(status="resolved").count()
    return render(request, "admin_reports.html", {
        "reports":        reports,
        "open_count":     open_count,
        "resolved_count": resolved_count,
    })


def resolve_report(request, id):
    """Mark a waste report as resolved."""
    if not request.user.is_staff:
        return redirect("/dashboard/")
    try:
        report = WasteReport.objects.get(id=id)
        report.status = "resolved"
        report.save()
        # Notify the reporter
        Notification.objects.create(
            user=report.user,
            message=f"✅ Your waste report at '{report.location}' has been resolved by the admin."
        )
    except WasteReport.DoesNotExist:
        pass
    return redirect("/admin-dashboard/reports/")


def admin_add_bin(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")

    if request.method == "POST":
        location   = request.POST.get("location", "").strip()
        latitude   = request.POST.get("latitude", "").strip()
        longitude  = request.POST.get("longitude", "").strip()
        fill_level = request.POST.get("fill_level", "0").strip()
        status     = request.POST.get("status", "empty")

        if not location or not latitude or not longitude:
            return render(request, "admin_add_bin.html", {
                "error": "Location, latitude and longitude are required.",
                "form_data": request.POST,
            })

        if SmartBin.objects.filter(location=location).exists():
            return render(request, "admin_add_bin.html", {
                "error": f"A bin at '{location}' already exists.",
                "form_data": request.POST,
            })

        SmartBin.objects.create(
            location=location,
            latitude=float(latitude),
            longitude=float(longitude),
            fill_level=int(fill_level) if fill_level.isdigit() else 0,
            status=status,
        )
        return redirect("/admin-dashboard/bins/")

    return render(request, "admin_add_bin.html")


def admin_edit_bin(request, id):
    if not request.user.is_staff:
        return redirect("/dashboard/")

    bin_obj = SmartBin.objects.get(id=id)

    if request.method == "POST":
        location   = request.POST.get("location", "").strip()
        latitude   = request.POST.get("latitude", "").strip()
        longitude  = request.POST.get("longitude", "").strip()
        fill_level = request.POST.get("fill_level", "0").strip()
        status     = request.POST.get("status", "empty")

        if not location or not latitude or not longitude:
            return render(request, "admin_edit_bin.html", {
                "error": "Location, latitude and longitude are required.",
                "bin": bin_obj,
            })

        # Check uniqueness (exclude self)
        if SmartBin.objects.filter(location=location).exclude(id=id).exists():
            return render(request, "admin_edit_bin.html", {
                "error": f"Another bin at '{location}' already exists.",
                "bin": bin_obj,
            })

        bin_obj.location   = location
        bin_obj.latitude   = float(latitude)
        bin_obj.longitude  = float(longitude)
        bin_obj.fill_level = int(fill_level) if fill_level.isdigit() else 0
        bin_obj.status     = status
        bin_obj.save()
        return redirect("/admin-dashboard/bins/")

    return render(request, "admin_edit_bin.html", {"bin": bin_obj})


def admin_delete_bin(request, id):
    if not request.user.is_staff:
        return redirect("/dashboard/")
    try:
        SmartBin.objects.get(id=id).delete()
    except SmartBin.DoesNotExist:
        pass
    return redirect("/admin-dashboard/bins/")


def feedback_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/feedback/")

    if request.method == "POST":
        message  = request.POST.get("message", "").strip()
        category = request.POST.get("category", "general")
        rating_raw = request.POST.get("rating", "")
        rating   = int(rating_raw) if rating_raw.isdigit() else None

        if not message:
            return render(request, "feedback.html", {"error": "Please write a message before submitting."})

        Feedback.objects.create(
            user=request.user,
            message=message,
            category=category,
            rating=rating,
        )
        return render(request, "feedback.html", {"success": True})

    return render(request, "feedback.html")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/profile/")

    total_reports    = WasteReport.objects.filter(user=request.user).count()
    open_reports     = WasteReport.objects.filter(user=request.user, status="open").count()
    resolved_reports = WasteReport.objects.filter(user=request.user, status="resolved").count()
    unread_notifs    = Notification.objects.filter(user=request.user, is_read=False).count()

    context = {
        "total_reports":    total_reports,
        "open_reports":     open_reports,
        "resolved_reports": resolved_reports,
        "unread_notifs":    unread_notifs,
    }

    return render(request, "profile.html", context)


def admin_feedback(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")
    from django.db.models import Avg
    feedbacks  = Feedback.objects.all().order_by("-created_at")
    avg_rating = feedbacks.aggregate(avg=Avg("rating"))["avg"]
    avg_rating = round(avg_rating, 1) if avg_rating else None
    return render(request, "admin_feedback.html", {
        "feedbacks":  feedbacks,
        "avg_rating": avg_rating,
    })


def admin_notifications(request):
    if not request.user.is_staff:
        return redirect("/dashboard/")
    notifications = Notification.objects.all().order_by("-created_at")
    unread_count  = notifications.filter(is_read=False).count()
    return render(request, "admin_notifications.html", {
        "notifications": notifications,
        "unread_count":  unread_count,
    })


def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/?next=/notifications/")

    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    unread_count  = notifications.filter(is_read=False).count()

    return render(request, "notifications.html", {
        "notifications": notifications,
        "unread_count":  unread_count,
    })


def mark_notifications_read(request):
    """Mark all of this user's notifications as read (POST)."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "not authenticated"}, status=401)

    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({"status": "ok"})


# ── Context processor helper (unread count in navbar) ──
# Used via template tag instead; see navbar.html approach
