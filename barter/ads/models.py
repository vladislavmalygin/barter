from django.db import models
from django.contrib.auth.models import User

from .constants import (MIDDLE_MAX_LENGTH,
                        LONG_MAX_LENGTH,
                        SHORT_MAX_LENGTH)

class Ad(models.Model):
    CONDITIONS = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=LONG_MAX_LENGTH)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=MIDDLE_MAX_LENGTH)
    condition = models.CharField(max_length=SHORT_MAX_LENGTH,
                                 choices=CONDITIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    ]

    ad_sender = models.ForeignKey(Ad, related_name='sent_proposals', on_delete=models.CASCADE)
    ad_receiver = models.ForeignKey(Ad, related_name='received_proposals', on_delete=models.CASCADE)

    comment = models.TextField()
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Предложение от {self.ad_sender} к {self.ad_receiver}"

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
