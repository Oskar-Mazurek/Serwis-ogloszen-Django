from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomerForm, AdForm
from .models import *


# Create your views here.

# strona główna
def showAllAds(request):
    today = date.today()
    AllAds = Ad.objects.filter(expirationDate__gte=today).order_by('expirationDate')
    images = AdImage.objects.all()
    return render(request, 'showAllAds.html', {'AllAds': AllAds, 'images': images})


# logowanie
def log(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'authenticationForm': AuthenticationForm(), })
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, 'Udało się zalogować')
            return redirect('showAllAds')
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Nie udało się zalogować, błędne dane logowania')
            return render(request, 'registration/login.html', {'authenticationForm': AuthenticationForm(), })


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html',
                      {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
    else:
        customerForm = CustomerForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password1'])
            except IntegrityError:
                messages.error(request,
                               'Spróbuj ponownie. Podany użytkownik istnieje już w bazie, popraw formularz rejestracji')
                return render(request, 'registration/register.html',
                              {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
            messages.success(request,
                             'Pomyślnie zarejestrowano!')  # komunikat ze success
            user.is_active = True
            user.save()
            if customerForm.is_valid():
                customer = customerForm.save(commit=False)
                customer.user = user
                customer.save()
                # return redirect login
                redirect('showAllAds')
            else:
                messages.error(request, 'Błąd w formularzu!')  # komunikat z bledem
                return render(request, 'registration/register.html',
                              {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
        else:
            messages.error(request, 'Błąd w formularzu!')  # komunikat z bledem
            return render(request, 'registration/register.html',
                          {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})
        return render(request, 'registration/register.html',
                      {'customerForm': CustomerForm(), 'userForm': UserCreationForm()})


@login_required
def logoutUser(request):
    logout(request)
    messages.error(request, 'Wylogowano')
    return redirect('showAllAds')


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    customer = get_object_or_404(Customer, user=user)
    today = date.today()
    userAds = Ad.objects.filter(customer=customer, expirationDate__gte=today).order_by('expirationDate')
    return render(request, "profile.html", {'userAds': userAds, 'customer': customer})


@login_required
def addAd(request):
    if request.method == 'GET':
        formAd = AdForm(request.POST or None)
        return render(request, "AdForm.html", {'formAd': formAd, })
    if request.method == 'POST':
        today = date.today()
        user = get_object_or_404(User, pk=request.user.id)
        customer = get_object_or_404(Customer, user=user)
        ad = Ad.objects.create(customer=customer, adName=request.POST['adName'],
                               description=request.POST['description'],
                               cost=request.POST['cost'], publicationDate=today,
                               expirationDate=today + timedelta(days=14))
        images = request.FILES.getlist('images')
        for image in images:
            AdImage.objects.create(ad=ad, image=image).save()
        ad.save()
        messages.success(request, 'Dodano ogłoszenie!')
    return redirect('profile')
