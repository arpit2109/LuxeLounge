from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    )
    
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)  # Fixed: Changed ROLE_CHOICES to ROOM_TYPES
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    quantity = models.IntegerField(default=1)
    amenities = models.JSONField(default=list)
    images = models.JSONField(default=list)
    three_d_model_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.room_type}"