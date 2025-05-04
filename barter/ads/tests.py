from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.ad_data = {
            'title': 'Новый велосипед',
            'description': 'Продаю новый велосипед, использовался один раз.',
            'image_url': 'http://example.com/image1.jpg',
            'category': 'Спорт',
            'condition': 'new'
        }
        self.ad = Ad.objects.create(user=self.user, **self.ad_data)

    def test_create_ad(self):
        response = self.client.post(reverse('ad-list'), self.ad_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)

    def test_edit_ad(self):
        response = self.client.put(reverse('ad-detail', args=[self.ad.id]), {
            'title': 'Обновленный велосипед',
            'description': 'Продаю обновленный велосипед.',
            'image_url': 'http://example.com/image2.jpg',
            'category': 'Спорт',
            'condition': 'new'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Обновленный велосипед')

    def test_delete_ad(self):
        response = self.client.delete(reverse('ad-detail', args=[self.ad.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_search_ads(self):
        Ad.objects.all().delete()
        self.ad = Ad.objects.create(user=self.user, title='велосипед', description='Описание', category='Спорт',
                                    condition='new')
        response = self.client.get(reverse('ad-list'), {'search': 'велосипед'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'велосипед')

class ExchangeProposalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.ad1 = Ad.objects.create(user=self.user, title='Объявление 1', description='Описание 1',
                                     category='Категория 1', condition='new')
        self.ad2 = Ad.objects.create(user=self.user, title='Объявление 2', description='Описание 2',
                                     category='Категория 2', condition='used')
        self.proposal_data = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Хочу обменяться.'
        }

    def test_create_proposal(self):
        self.ad1 = Ad.objects.create(user=self.user, title='Объявление 1', description='Описание 1',
                                     category='Категория 1', condition='new')
        self.ad2 = Ad.objects.create(user=self.user, title='Объявление 2', description='Описание 2',
                                     category='Категория 2', condition='used')

        response = self.client.post(reverse('exchangeproposal-list'), self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)

    def test_update_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2,
                                                   comment='Первое предложение')
        response = self.client.put(reverse('exchangeproposal-detail', args=[proposal.id]), {
            'status': 'accepted',
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': proposal.comment
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')

    def test_delete_proposal(self):
        proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, comment='Первое предложение')
        response = self.client.delete(reverse('exchangeproposal-detail', args=[proposal.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExchangeProposal.objects.count(), 0)
