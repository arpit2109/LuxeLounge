from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count
from .models import Room
from .serializers import RoomSerializer
from bookings.models import Booking

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['room_type', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price_per_night', 'capacity']

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
@permission_classes([AllowAny])
def check_availability(request, room_id):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if not check_in or not check_out:
        return Response({'error': 'Both check_in and check_out dates are required'}, status=400)
    
    try:
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
        available_quantity = max(0, room.quantity - booked_count)
        is_available = available_quantity > 0
        
        return Response({
            'room_id': room_id,
            'check_in': check_in,
            'check_out': check_out,
            'is_available': is_available,
            'available_quantity': available_quantity,
            'total_quantity': room.quantity,
            'message': f'Room is available. {available_quantity} left.' if is_available else 'Room is not available for these dates'
        })
        
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)