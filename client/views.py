from django.shortcuts import render
from netball.models import Fixture


# Create your views here.
def Home(request):

    return render(request, "base/home.html")
