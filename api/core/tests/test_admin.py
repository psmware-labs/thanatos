from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Account


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@psmware.io',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@psmware.io',
            password='password123',
            name='Test user full name'
        )
        self.account = Account.objects.create(user=self.user, name='SAP')

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # above line generates url like   /admin/core/user/17 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_accounts_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_account_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.account.name)

    def test_account_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_account_change', args=[self.account.id])
        # above line generates url like   /admin/core/user/17 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_create_account_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_account_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)
