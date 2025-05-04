from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .serializers import AdSerializer, ExchangeProposalSerializer
from .models import Ad, ExchangeProposal
from .pagination import PagePagination


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('created_at')
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PagePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        condition = self.request.query_params.get('condition', None)
        search = self.request.query_params.get('search', None)

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_ad(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def edit_ad(self, request, pk=None):
        ad = self.get_object()
        if ad.user != request.user:
            return Response({"detail": "У вас нет прав на редактирование этого объявления."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_ad(self, request, pk=None):
        ad = self.get_object()
        if ad.user != request.user:
            return Response({"detail": "У вас нет прав на удаление этого объявления."},
                            status=status.HTTP_403_FORBIDDEN)

        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        ad_sender_id = self.request.query_params.get('ad_sender_id', None)
        ad_receiver_id = self.request.query_params.get('ad_receiver_id', None)
        status = self.request.query_params.get('status', None)

        if ad_sender_id:
            queryset = queryset.filter(ad_sender__id=ad_sender_id)

        if ad_receiver_id:
            queryset = queryset.filter(ad_receiver__id=ad_receiver_id)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.filter(Q(ad_sender__user=user) | Q(ad_receiver__user=user))

        return queryset

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_proposal(self, request):
        ad_sender_id = request.data.get('ad_sender_id')
        ad_receiver_id = request.data.get('ad_receiver_id')
        comment = request.data.get('comment')

        try:
            ad_sender = Ad.objects.get(id=ad_sender_id)
            ad_receiver = Ad.objects.get(id=ad_receiver_id)
        except Ad.DoesNotExist:
            return Response({"detail": "Одно из объявлений не найдено."}, status=status.HTTP_404_NOT_FOUND)

        proposal = ExchangeProposal(
            ad_sender=ad_sender,
            ad_receiver=ad_receiver,
            comment=comment
        )
        proposal.save()

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def update_proposal(self, request, pk=None):
        proposal = self.get_object()
        status = request.data.get('status')

        if status not in dict(ExchangeProposal.STATUS_CHOICES):
            return Response({"detail": "Неверный статус."}, status=status.HTTP_400_BAD_REQUEST)

        proposal.status = status
        proposal.save()

        serializer = self.get_serializer(proposal)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def list_proposals(self, request):

        user = request.user
        proposals = ExchangeProposal.objects.filter(
            Q(ad_sender__user=user) | Q(ad_receiver__user=user)
        )
        serializer = self.get_serializer(proposals, many=True)
        return Response(serializer.data)
