from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile


# ================= HOME =================

def home(request):
    return render(request, "home.html")


# ================= LOGIN =================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:

            # Email is stored in Django User model
            user = User.objects.get(email=email)

            # Check password
            if user.check_password(password):

                login(request, user)

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Incorrect password."
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "No account found with this email."
            )

    return render(request, "login.html")


# ================= DASHBOARD =================

@login_required(login_url="login")
def dashboard(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    context = {

        "profile": profile,

        "user": request.user,

    }

    return render(
        request,
        "dashboard.html",
        context
    )


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")