from datetime import date

from django.shortcuts import render
from .models import *


# Create your views here.

def showAllAds(request):
    today = date.today()
    AllAds = Ad.objects.all().order_by('publicationDate')

    return render(request, 'showAllAds.html', {'AllAds': AllAds})
