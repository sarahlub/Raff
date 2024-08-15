from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Raffle, Ticket, Winner

admin.site.register(Raffle)
admin.site.register(Ticket)
admin.site.register(Winner)