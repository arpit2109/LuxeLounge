from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("Booking creation request data:", request.data)
        
        # Add the user to the request data
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = False
        
        # Check room availability before creating booking
        room_id = request.data.get('room')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        
        try:
            from rooms.models import Room
            room = Room.objects.get(id=room_id)
            
            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                room=room,
                check_out__gt=check_in,
                check_in__lt=check_out,
                status__in=['confirmed', 'pending']
            )
            
            # Calculate available quantity
            booked_count = overlapping_bookings.count()
            if booked_count >= room.quantity:
                return Response(
                    {'error': 'No rooms available for the selected dates'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Room.DoesNotExist:
            return Response(
                {'error': 'Room not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        
        nights = (check_out - check_in).days
        total_price = room.price_per_night * nights
        
        serializer.save(user=self.request.user, total_price=total_price)

# ... rest of the views code ...
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class UserBookingsListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class AllBookingsListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Booking.objects.all()