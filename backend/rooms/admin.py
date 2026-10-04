from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'price_per_night', 'capacity', 'is_available']
    list_filter = ['room_type', 'is_available']
    search_fields = ['name', 'description']