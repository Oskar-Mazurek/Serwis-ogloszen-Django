from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from . import views

urlpatterns = [
                  path('', views.showAllAds, name='showAllAds'),
                  path('login/', views.log, name='login'),
                  path('rejestracja/', views.register, name='register'),
                  path('logout/', views.logoutUser, name='logout'),
                  path('profil/', views.profile, name='profile'),
                  path('addAd/', views.addAd, name='addAd'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
