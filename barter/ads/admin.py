from django.contrib import admin
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'condition', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('condition', 'category')


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('ad_sender', 'ad_receiver', 'status', 'created_at')
    search_fields = ('ad_sender__title', 'ad_receiver__title', 'comment')
    list_filter = ('status',)
