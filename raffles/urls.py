# raffles/urls.py
from django.urls import path
from .views import (
    RaffleCreateView, RaffleListView, RaffleDetailView, RaffleParticipateView,
    RaffleDrawWinnersView, RaffleWinnersListView, VerifyTicketView
)

urlpatterns = [
    path('raffles/', RaffleListView.as_view(), name='raffle-list'),
    path('raffles/create/', RaffleCreateView.as_view(), name='raffle-create'),
    path('raffles/<int:pk>/', RaffleDetailView.as_view(), name='raffle-detail'),
    path('raffles/<int:id>/participate/', RaffleParticipateView.as_view(), name='raffle-participate'),
    path('raffles/<int:id>/winners/', RaffleDrawWinnersView.as_view(), name='raffle-draw-winners'),
    path('raffles/<int:id>/winners/list/', RaffleWinnersListView.as_view(), name='raffle-winners-list'),
    path('raffles/<int:id>/verify-ticket/', VerifyTicketView.as_view(), name='verify-ticket'),
]



