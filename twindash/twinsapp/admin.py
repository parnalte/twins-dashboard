from django.contrib import admin

# Register your models here.
from .models import Bebe, Toma, Cambio

admin.site.register(Bebe)
admin.site.register(Toma)
admin.site.register(Cambio)
