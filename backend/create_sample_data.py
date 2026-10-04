import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LuxeLounge.settings')
django.setup()

from rooms.models import Room
from authentication.models import CustomUser

# Create sample rooms
rooms_data = [
    {
        'name': 'Luxury Suite',
        'room_type': 'suite',
        'description': 'Spacious suite with ocean view and premium amenities',
        'price_per_night': 299.99,
        'capacity': 3,
        'amenities': ['WiFi', 'TV', 'Air Conditioning', 'Mini Bar', 'Ocean View'],
        'images': ['/media/room1.jpg', '/media/room2.jpg'],
        'three_d_model_url': '/media/3d/suite.glb',
        'is_available': True
    },
    {
        'name': 'Deluxe Room',
        'room_type': 'deluxe',
        'description': 'Comfortable room with city view and modern amenities',
        'price_per_night': 199.99,
        'capacity': 2,
        'amenities': ['WiFi', 'TV', 'Air Conditioning', 'Coffee Maker'],
        'images': ['/media/deluxe1.jpg', '/media/deluxe2.jpg'],
        'three_d_model_url': '/media/3d/deluxe.glb',
        'is_available': True
    },
    {
        'name': 'Standard Room',
        'room_type': 'standard',
        'description': 'Cozy room with all essential amenities',
        'price_per_night': 129.99,
        'capacity': 2,
        'amenities': ['WiFi', 'TV', 'Air Conditioning'],
        'images': ['/media/standard1.jpg', '/media/standard2.jpg'],
        'is_available': True
    }
]

for room_data in rooms_data:
    Room.objects.create(**room_data)

print("Sample rooms created successfully!")