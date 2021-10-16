from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import User, UserInterest


class UserAdmin(LeafletGeoAdmin):
    list_display = (
        'id',
        'username',
        'last_location',
        'email',
        'city',
    )


admin.site.site_header = 'Fitness Buddy'
admin.site.register(User, UserAdmin)
admin.site.register(UserInterest)