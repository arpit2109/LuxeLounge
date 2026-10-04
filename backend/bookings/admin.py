from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'check_in', 'check_out', 'status', 'total_price']
    list_filter = ['status', 'room__room_type']
    search_fields = ['user__username', 'room__name']