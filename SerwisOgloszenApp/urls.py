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
                  path('editAd/<int:id>', views.editAd, name='editAd'),
                  path('deleteAd/<int:id>', views.deleteAd, name='deleteAd'),
                  path('adDetails/<int:id>', views.adDetails, name='adDetails'),
                  path('search/', views.search, name='search'),
                  path('reserveAd/<int:adId>', views.reserveAd, name='reserveAd'),
                  path('cancelReservation/<int:id>', views.cancelReservation, name='cancelReservation'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
