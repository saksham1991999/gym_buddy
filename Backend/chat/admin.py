
from django.contrib import admin

from .models import ReportGroup, Room, RoomUser, Message
import nested_admin


class RoomUserInline(nested_admin.NestedTabularInline):
    model = RoomUser
    extra = 0


class RoomAdmin(nested_admin.NestedModelAdmin):
    inlines = [RoomUserInline]
    list_display = [
                    'id',
                    'name',
                    'title',
                    'created_at',
                    'deleted_at',
                    ]
    list_editable = [
                    ]
    list_display_links = [
                    'id',
                    'name',
                    'title',
                    ]
    list_filter = [

                    ]
    search_fields = [
                    'name',
                    'title',
                    'description',
                    ]


class RoomMessageAdmin(nested_admin.NestedModelAdmin):
    list_display = [
                    'id',
                    'room',
                    'user',
                    'created_on',
                    'message_text',
                    ]
    list_editable = [
                    ]
    list_display_links = [
                    'id',
                    'room',
                    'user',
                    'created_on',
                    'message_text',
                    ]
    list_filter = [
                    'room',
                    'user',
                    ]
    search_fields = [
                    'room',
                    'user',
                    'message_text',
                    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(RoomUser)
admin.site.register(Message, RoomMessageAdmin)
admin.site.register(ReportGroup)