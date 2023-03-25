from django.urls import path

from . import views

urlpatterns = [
    path('', views.showAllAds, name='showAllAds'),
    path('login/', views.log, name='login'),
    path('rejestracja/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profil/', views.profile, name='profile'),
]
