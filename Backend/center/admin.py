from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import CenterType, Center, CenterImages


class CenterImageInline(admin.TabularInline):
    model = CenterImages
    extra = 0


class CenterAdmin(LeafletGeoAdmin):
    inlines = [
        CenterImageInline
    ]
    list_display = (
        'id',
        'type',
        'name',
        'contact_name',
        'location',
        'city',
        'state',
    )
    list_display_links = [
        'id',
        'type',
        'name',
        'contact_name',
        'location',
        'city',
    ]
    search_fields = [
        'name',
        'contact_name',
        'contact',
        'location',
        'city',
    ]
    list_filter = [
        'type',
        'city',
        'state',
    ]


admin.site.register(CenterType)
admin.site.register(Center, CenterAdmin)
admin.site.register(CenterImages)