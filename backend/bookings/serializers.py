from rest_framework import serializers
from .models import Booking
from rooms.serializers import RoomSerializer
from authentication.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    room_details = RoomSerializer(source='room', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'total_price', 'status', 'user')

    def validate(self, data):
        print("Booking validation data:", data)
        
        # Check if check_out is after check_in
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        
        # Check if booking is for future dates
        from django.utils import timezone
        if data['check_in'] < timezone.now().date():
            raise serializers.ValidationError("Cannot book for past dates.")
        
        return data