from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomerForm, AdForm, AdEditForm
from .models import *


# Create your views here.

# strona główna
def showAllAds(request):
    today = datetime.now()
    AllAds = Ad.objects.filter(expirationDate__gte=today, taken=False).order_by('expirationDate')
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
    userAds = Ad.objects.filter(customer=customer, expirationDate__gte=today).order_by('-taken', 'expirationDate')
    reservedAds = Ad.objects.filter(reserver=customer, expirationDate__gte=today).order_by('expirationDate')
    return render(request, "profile.html",
                  {'userAds': userAds, 'customer': customer, 'reservedAds': reservedAds})


@login_required
def addAd(request):
    if request.method == 'GET':
        formAd = AdForm(request.POST or None)
        return render(request, "AdForm.html", {'formAd': formAd, })
    if request.method == 'POST':
        today = datetime.now()
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


def editAd(request, id):
    ad = get_object_or_404(Ad, pk=id)
    editAdForm = AdEditForm(request.POST or None, request.FILES or None, instance=ad)

    if editAdForm.is_valid():
        editAdForm.save()
        messages.success(request, 'Edycja ogłoszenia udana!')
        return redirect('profile')

    return render(request, 'editAd.html', {'editAdForm': editAdForm, 'ad': ad})


def deleteAd(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if request.method == "POST":
        ad.delete()
        messages.error(request, 'Usunięto ogłoszenie!')
        return redirect('profile')

    return render(request, 'deleteAdConfirm.html', {'ad': ad})


def adDetails(request, id):
    ad = get_object_or_404(Ad, pk=id)
    images = AdImage.objects.all()
    return render(request, 'adDetails.html', {'ad': ad, 'images': images})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        today = datetime.now()
        results = Ad.objects.filter(adName__contains=searched, expirationDate__gte=today, taken=False).order_by(
            'expirationDate')
        images = AdImage.objects.all()
        return render(request, 'search.html', {'searched': searched, 'results': results, 'images': images})
    else:
        return render(request, 'search.html', {})


@login_required()
def reserveAd(request, adId):
    if request.method == "POST":
        ad = get_object_or_404(Ad, pk=adId)
        loggedUser = get_object_or_404(User, pk=request.user.id)
        loggedcustomer = get_object_or_404(Customer, user=loggedUser)
        ad.reserver = loggedcustomer
        ad.taken = True
        ad.save()
        messages.success(request, 'Zarezerwowano ogłoszenie, skontaktuj się z właścicielem ogłoszenia!')
        return redirect('profile')
    else:
        ad = get_object_or_404(Ad, pk=adId)
        return render(request, 'reserveAd.html', {'ad': ad})


def cancelReservation(request, id):
    ad = get_object_or_404(Ad, pk=id)
    if request.method == "POST":
        ad.taken = False
        ad.reserver = None
        ad.save()
        messages.success(request, 'Zrezygnowano z rezerwacji ogłoszenia!')
        return redirect('profile')

    return render(request, 'cancelReservation.html', {'ad': ad})
