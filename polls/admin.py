
from django.contrib import admin

from .models import Profile, Bookings

class bookingsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'date_time', 'stats')

class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')

admin.site.register(Profile, profileAdmin)
admin.site.register(Bookings, bookingsAdmin)


