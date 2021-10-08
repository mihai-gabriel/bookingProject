from django.contrib import admin

from .models import Hotel, Room, Order

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Order)
