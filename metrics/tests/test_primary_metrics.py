from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import PrimaryMetric

from metrics.serializers import PrimaryMetricSerializer


PRIMARY_METRIC_URL = reverse('metrics:primarymetric-list')


class PublicPrimaryMetricsApiTests(TestCase):
    """Test the publicly available primary_metrics API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving primary_metrics"""
        res = self.client.get(PRIMARY_METRIC_URL)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePrimaryMetricsApiTests(TestCase):
    """Test the authorized user primary_metrics API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@psmware.io',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_primary_metrics(self):
        """Test retrieving primary_metrics"""
        PrimaryMetric.objects.create(
            user=self.user, metric='Architectural Stability')
        PrimaryMetric.objects.create(user=self.user, metric='Tooling')

        res = self.client.get(PRIMARY_METRIC_URL)

        primary_metrics = PrimaryMetric.objects.all().order_by('-metric')
        serializer = PrimaryMetricSerializer(primary_metrics, many=True)
        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_primary_metric_successful(self):
        """Test creating a new primary_metric"""
        payload = {'metric': 'Tooling'}
        self.client.post(PRIMARY_METRIC_URL, payload)

        exists = PrimaryMetric.objects.filter(
            user=self.user,
            metric=payload['metric']
        ).exists()
        # Assertion
        self.assertTrue(exists)

    def test_create_primary_metric_invalid(self):
        """Test creating a new primary_metric with invalid payload"""
        payload = {'metric': ''}
        res = self.client.post(PRIMARY_METRIC_URL, payload)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
