from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from authentication.models import CustomUser
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Check if check-out is after check-in
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out date must be after check-in date.")
        
        # Check if booking is for future dates
        if self.check_in < timezone.now().date():
            raise ValidationError("Cannot book for past dates.")
        
        # Check room availability
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_out__gt=self.check_in,
            check_in__lt=self.check_out,
            status__in=['confirmed', 'pending']
        ).exclude(pk=self.pk)
        
        if overlapping_bookings.exists():
            raise ValidationError("This room is not available for the selected dates.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"