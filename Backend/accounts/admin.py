from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import User, UserInterest


class UserAdmin(LeafletGeoAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_location',
        'email',
        'city',
        'type',
        'active',
    )
    list_display_links = [
        'id',
        'username',
        'last_location',
        'email',
        'city',
    ]
    search_fields = [
        'username',
        'email',
        'city',
    ]
    list_filter = [
        'city',
        'type',
        'active',
    ]


admin.site.site_header = 'Fitness Buddy'
admin.site.register(User, UserAdmin)
admin.site.register(UserInterest)