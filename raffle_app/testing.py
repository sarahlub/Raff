from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Raffle

class RaffleTests(APITestCase):
    def test_create_raffle(self):
        url = reverse('raffle-list')  # Adjust to your URL name
        data = {
            'number_of_tickets': 100,
            'prizes': ['Prize 1', 'Prize 2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Raffle.objects.count(), 1)
        self.assertEqual(Raffle.objects.get().number_of_tickets, 100)
