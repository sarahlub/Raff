# raffles/models.py
from django.db import models
from django.contrib.auth.models import User
import hashlib
import random

class Raffle(models.Model):
    name = models.CharField(max_length=100)
    total_tickets = models.PositiveIntegerField()
    prizes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    raffle = models.ForeignKey(Raffle, related_name='tickets', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    participant_ip = models.GenericIPAddressField()
    verification_code = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = hashlib.sha256(f'{self.number}-{random.random()}'.encode()).hexdigest()
        super().save(*args, **kwargs)

from django.db import models

class Winner(models.Model):
    raffle = models.ForeignKey('Raffle', on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    prize = models.CharField(max_length=255)
    # Other fields

    def __str__(self):
        return f'{self.ticket} - {self.prize}'

