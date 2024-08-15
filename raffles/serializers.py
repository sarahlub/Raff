
from rest_framework import serializers
from .models import Raffle, Ticket, Winner

class RaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = '__all__'
