from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Account

from accounts.serializers import AccountSerializer


ACCOUNT_URL = reverse('accounts:account-list')


class PublicAccountsApiTests(TestCase):
    """Test the publicly available accounts API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving accounts"""
        res = self.client.get(ACCOUNT_URL)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAccountsApiTests(TestCase):
    """Test the authorized user accounts API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@psmware.io',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_accounts(self):
        """Test retrieving accounts"""
        Account.objects.create(
            user=self.user, name='SAP')
        Account.objects.create(user=self.user, name='BSNIC')

        res = self.client.get(ACCOUNT_URL)

        accounts = Account.objects.all().order_by('name')
        serializer = AccountSerializer(accounts, many=True)
        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_account_successful(self):
        """Test creating a new account"""
        payload = {'name': 'BSNIC'}
        self.client.post(ACCOUNT_URL, payload)

        exists = Account.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        # Assertion
        self.assertTrue(exists)

    def test_create_account_invalid(self):
        """Test creating a new account with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(ACCOUNT_URL, payload)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
