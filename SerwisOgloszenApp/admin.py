from django.contrib import admin
from .models import Customer, Ad, AdImage

# Register your models here.
admin.site.register(Customer)


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 5


class AdAdmin(admin.ModelAdmin):
    inlines = [AdImageInline, ]


admin.site.register(Ad, AdAdmin)
