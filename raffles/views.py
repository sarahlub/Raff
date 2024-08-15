# raffles/views.py
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Raffle, Ticket, Winner
from .serializers import RaffleSerializer, TicketSerializer, WinnerSerializer
import random
from django.conf import settings

def is_manager(request):
    return request.META['REMOTE_ADDR'] in settings.MANAGER_IPS

class RaffleCreateView(generics.CreateAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

    def post(self, request, *args, **kwargs):
        if not is_manager(request):
            raise PermissionDenied("You are not allowed to create raffles.")
        return super().post(request, *args, **kwargs)

class RaffleListView(generics.ListAPIView):
    queryset = Raffle.objects.all().order_by('-created_at')
    serializer_class = RaffleSerializer

class RaffleDetailView(generics.RetrieveAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer

class RaffleParticipateView(views.APIView):
    def post(self, request, id):
        raffle = Raffle.objects.get(id=id)
        if Ticket.objects.filter(raffle=raffle, participant_ip=request.META['REMOTE_ADDR']).exists():
            return Response({'error': 'This IP address has already participated.'}, status=status.HTTP_400_BAD_REQUEST)
        available_tickets = list(set(range(1, raffle.total_tickets + 1)) - set(Ticket.objects.filter(raffle=raffle).values_list('number', flat=True)))
        if not available_tickets:
            return Response({'error': 'No tickets available.'}, status=status.HTTP_400_BAD_REQUEST)
        ticket_number = random.choice(available_tickets)
        ticket = Ticket.objects.create(raffle=raffle, number=ticket_number, participant_ip=request.META['REMOTE_ADDR'])
        return Response(TicketSerializer(ticket).data)

class RaffleDrawWinnersView(views.APIView):
    def post(self, request, id):
        if not is_manager(request):
            raise PermissionDenied("You are not allowed to draw winners.")
        raffle = Raffle.objects.get(id=id)
        if Winner.objects.filter(raffle=raffle).exists():
            return Response({'error': 'Winners have already been drawn.'}, status=status.HTTP_400_BAD_REQUEST)
        tickets = list(Ticket.objects.filter(raffle=raffle))
        random.shuffle(tickets)
        winners = []
        for prize in raffle.prizes:
            if not tickets:
                break
            ticket = tickets.pop()
            winner = Winner.objects.create(raffle=raffle, ticket=ticket, prize=prize)
            winners.append(winner)
        return Response(WinnerSerializer(winners, many=True).data)

class RaffleWinnersListView(generics.ListAPIView):
    serializer_class = WinnerSerializer

    def get_queryset(self):
        raffle_id = self.kwargs['id']
        return Winner.objects.filter(raffle__id=raffle_id)

class VerifyTicketView(views.APIView):
    def post(self, request, id):
        raffle = Raffle.objects.get(id=id)
        ticket_number = request.data.get('ticket_number')
        verification_code = request.data.get('verification_code')
        try:
            ticket = Ticket.objects.get(raffle=raffle, number=ticket_number)
            if ticket.verification_code == verification_code:
                return Response({'valid': True})
            else:
                return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)
