from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(
      User, on_delete=models.CASCADE,
      null=False, blank=False
    )
    book_date = models.DateField('date booked', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_date', 'user'], name='user_book_date')
        ]
