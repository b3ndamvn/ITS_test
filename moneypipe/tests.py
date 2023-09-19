import decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase

from .models import MoneyUser


class MoneyUserTests(APITestCase):
    def setUp(self) -> None:
        MoneyUser.objects.create(name='Ivan', lastname='Ivanov', INN='123456789012', balance='10')

    def test_get_moneyuser_list(self):
        url = reverse('get_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {"id": 1, "name": "Ivan", "lastname": "Ivanov", "INN": "123456789012", "balance": "10.00"}
        ])

    def test_create_moneyuser(self):
        url = reverse('get_users')
        data = {
            "name": "string",
            "lastname": "string",
            "INN": "069836447176",
            "balance": "10"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_inn_moneyuser(self):
        url = reverse('get_users')
        data = {
            "name": "string",
            "lastname": "string",
            "INN": "06983644717",
            "balance": "string"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_balance_moneyuser(self):
        url = reverse('get_users')
        data = {
            "name": "string",
            "lastname": "string",
            "INN": "069836447171",
            "balance": "1.2a"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_inn_moneyuser(self):
        url = reverse('get_users')
        data = [
            {
                "name": "Petr",
                "lastname": "Petrov",
                "INN": "567890123456",
                "balance": "10"
            },
            {
                "name": "Maria",
                "lastname": "Smirnova",
                "INN": "567890123456",
                "balance": "15"
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SendMoneyTests(APITestCase):
    def setUp(self) -> None:
        MoneyUser.objects.create(name='Ivan', lastname='Ivanov', INN='123456789012', balance='10')
        MoneyUser.objects.create(name='Lilly', lastname='Lilly', INN='223456789012', balance='0')
        MoneyUser.objects.create(name='Nick', lastname='Nick', INN='323456789012', balance='0')
        MoneyUser.objects.create(name='Name', lastname='Lastname', INN='423456789012', balance='0')

    def test_send_money(self):
        url = reverse('send_money')
        data = {
            "source": 1,
            "destination": [
                "223456789012",
                "323456789012",
                "423456789012"
            ],
            "value": "10"
        }
        response = self.client.post(url, data, format='json')
        source = MoneyUser.objects.filter(pk=1).first()
        destination = MoneyUser.objects.filter(INN__in=data.get('destination'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(source.balance, decimal.Decimal('0.01'))
        self.assertEqual([bal.balance for bal in destination], list(map(decimal.Decimal, ['3.33', '3.33', '3.33'])))

    def test_no_balance_send_money(self):
        url = reverse('send_money')
        data = {
            "source": 1,
            "destination": [
                "223456789012",
                "323456789012",
                "423456789012"
            ],
            "value": "20"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_inn_send_money(self):
        url = reverse('send_money')
        data = {
            "source": 1,
            "destination": [
                "823456789012",
                "323456789012",
                "423456789012"
            ],
            "value": "5"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
