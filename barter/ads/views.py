from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]
