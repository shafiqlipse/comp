from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from accounts.models import Championship
from django.contrib import messages
from .forms import *
from django.http import HttpRequest, HttpResponse
from .models import *
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from accounts.decorators import school_required, anonymous_required
from .forms import RegistrationForm





@anonymous_required
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user without logging in
            user = form.get_user()
            login(request, user)

            # Check if the user is a school

            # If the user is not a school, log in and redirect to dashboard
            messages.success(request, "Login successful.")
            return redirect("dashboard")  # Adjust the URL name for your dashboard view
        else:
            messages.error(request, "Error in login. Please check your credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    # if user.is_authenticated:
    logout(request)
    return redirect("login")


def custom_404(request, exception):
    return render(request, "account/custom404.html", {}, status=404)


# championships
def schools(request):
    schools = School.objects.all()
    new_school = None

    if request.method == "POST":
        sform = SchoolForm(request.POST, request.FILES)

        if sform.is_valid():
            new_school = sform.save(commit=False)

            new_school.save()
            return redirect("schools")
    else:
        sform = SchoolForm()
    context = {"schools": schools, "sform": sform}
    return render(request, "school/schools.html", context)


# add championships


def schoolDetail(request, id):
    school = School.objects.get(id=id)
    athletes = Athlete.objects.filter(school=school)
    new_athlete = None

    if request.method == "POST":
        cform = AthleteForm(request.POST, request.FILES)

        if cform.is_valid():
            new_athlete = cform.save(commit=False)
            new_athlete.school = school

            new_athlete.save()
            return redirect("schoolDetail", school.id)
    else:
        cform = AthleteForm()

    context = {
        "school": school,
        "athletes": athletes,
        "cform": cform,
    }

    return render(request, "school/school.html", context)


def AthleteDetail(request, id):
    athlete = Athlete.objects.get(id=id)

    context = {
        "athlete": athlete,
    }

    return render(request, "school/athlete.html", context)
