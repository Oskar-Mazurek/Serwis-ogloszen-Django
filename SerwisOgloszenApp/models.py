from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    USER_TYPES = (('ADM', 'Administrator'), ('U', 'User'))
    userType = models.CharField(max_length=3, choices=USER_TYPES, default='U')
    name = models.CharField(max_length=20)
    surName = models.CharField(max_length=40)
    telNum = models.IntegerField(verbose_name='Numer telefonu', null=False, blank=False)
    street = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    zipCode = models.CharField(max_length=6)
    state = models.CharField(max_length=20)

    def displayUserType(self):
        if self.userType == 'ADM':
            return "Administrator"
        if self.userType == 'U':
            return "Użytkownik"

    def __str__(self):
        if self.userType == 'ADM':
            return "Nazwa użytkownika:" + self.user.username + " Typu: Administrator"
        if self.userType == 'U':
            return "Nazwa użytkownika:" + self.user.username + " Typu: Użytkownik"


class Ad(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
    adName = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=2000, null=False, blank=False)
    cost = models.FloatField(verbose_name='Cena', null=False, blank=False)
    publicationDate = models.DateTimeField()
    expirationDate = models.DateTimeField()
    taken = models.BooleanField(default=False)
    reserver = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE, default="",
                                    related_name='reserver')

    def __str__(self):
        return "ID:" + str(self.pk) + \
               "Nazwa ogłoszenia: " + str(self.adName) + \
               " Cena: " + str(self.cost) + \
               " Data publikacji: " + str(self.publicationDate + timedelta(hours=2)) + \
               " Data przedawnienia: " + str(self.expirationDate + timedelta(hours=2)) + \
               " Kto opublikował: " + str(self.customer.user.username)


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="adImages", null=False, blank=False)
