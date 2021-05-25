from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Account, PrimaryMetric, \
    Question, SecondaryMetric, TertiaryMetric


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
        self.primary_metric = PrimaryMetric.objects.create(
            user=self.user, metric='SAP primary_metric')
        self.secondary_metric = SecondaryMetric.objects.create(
            user=self.user, metric='SAP secondary_metric')
        self.tertiary_metric = TertiaryMetric.objects.create(
            user=self.user, metric='SAP secondary_metric')

        self.question = Question.objects.create(
            user=self.user,
            primary_metric=self.primary_metric,
            secondary_metric=self.secondary_metric,
            tertiary_metric=self.tertiary_metric
        )

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
        """Test that accounts are listed on user page"""
        url = reverse('admin:core_account_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.account.name)

    def test_account_change_page(self):
        """Test that the account edit page works"""
        url = reverse('admin:core_account_change', args=[self.account.id])
        # above line generates url like /admin/core/account/17 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_create_account_page(self):
        """Test that the create account page works"""
        url = reverse('admin:core_account_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_primary_metric_listed(self):
        """Test that the primary metrics are listed on primarymetrics page"""
        url = reverse('admin:core_primarymetric_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.primary_metric.metric)

    def test_primary_metric_change_page(self):
        """Test that the primary_metric edit page works"""
        url = reverse('admin:core_primarymetric_change',
                      args=[self.primary_metric.id])
        # above line generates url like /admin/core/primarymetric/1 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_primary_metric_account_page(self):
        """Test that the create primary_metric page works"""
        url = reverse('admin:core_primarymetric_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_secondary_metric_listed(self):
        """Test that the secondary metrics are listed on
        secondarymetrics page"""
        url = reverse('admin:core_secondarymetric_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.secondary_metric.metric)

    def test_secondary_metric_change_page(self):
        """Test that the secondary_metric edit page works"""
        url = reverse('admin:core_secondarymetric_change',
                      args=[self.secondary_metric.id])
        # above line generates url like /admin/core/secondarymetric/1 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_secondary_metric_account_page(self):
        """Test that the create secondary_metric page works"""
        url = reverse('admin:core_secondarymetric_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_tertiary_metric_listed(self):
        """Test that the tertiary metrics are listed on tertiarymetrics page"""
        url = reverse('admin:core_tertiarymetric_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.tertiary_metric.metric)

    def test_tertiary_metric_change_page(self):
        """Test that the tertiary edit page works"""
        url = reverse('admin:core_tertiarymetric_change',
                      args=[self.tertiary_metric.id])
        # above line generates url like /admin/core/tertiarymetric/1 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_tertiary_metric_account_page(self):
        """Test that the create tertiary metric page works"""
        url = reverse('admin:core_tertiarymetric_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_question_listed(self):
        """Test that the questions are listed on questions page"""
        url = reverse('admin:core_question_changelist')
        res = self.client.get(url)
        # Assertions
        self.assertContains(res, self.question)

    def test_question_metric_change_page(self):
        """Test that the question edit page works"""
        url = reverse('admin:core_question_change',
                      args=[self.question.id])
        # above line generates url like /admin/core/questions/1 (id)
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)

    def test_question_page(self):
        """Test that the create question page works"""
        url = reverse('admin:core_tertiarymetric_add')
        res = self.client.get(url)
        # Assertions ( checking for http 200 )
        self.assertEqual(res.status_code, 200)
