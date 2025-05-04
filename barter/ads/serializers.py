from rest_framework import serializers

from .models import Ad, ExchangeProposal

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id',
                  'title',
                  'description',
                  'image_url',
                  'category',
                  'condition',
                  'created_at',)
        read_only_fields = ('id', 'created_at',)

class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ('id',
                  'ad_sender',
                  'ad_receiver',
                  'comment',
                  'status',
                  'created_at',)
