# Generated by Django 3.2.18 on 2023-03-17 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(choices=[('ADM', 'Administrator'), ('U', 'User')], default='U', max_length=3)),
                ('name', models.CharField(max_length=20)),
                ('surName', models.CharField(max_length=40)),
                ('telNum', models.IntegerField(verbose_name='Numer telefonu')),
                ('street', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('zipCode', models.CharField(max_length=6)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adName', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('cost', models.FloatField(verbose_name='Cena')),
                ('publicationDate', models.DateTimeField()),
                ('expirationDate', models.DateTimeField()),
                ('image', models.ImageField(upload_to='adImages')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SerwisOgloszenApp.customer')),
            ],
        ),
    ]
