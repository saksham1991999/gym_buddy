from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import User


class UserAdmin(LeafletGeoAdmin):
    list_display = (
        'username',
        'last_location',
        'email',
        'city',
    )


admin.site.site_header = 'Fitness Buddy'
admin.site.register(User, UserAdmin)