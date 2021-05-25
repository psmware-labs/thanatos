from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import TertiaryMetric

from metrics.serializers import TertiaryMetricSerializer


PRIMARY_METRIC_URL = reverse('metrics:tertiarymetric-list')


class PublicTertiaryMetricsApiTests(TestCase):
    """Test the publicly available tertiary_metrics API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tertiary_metrics"""
        res = self.client.get(PRIMARY_METRIC_URL)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTertiaryMetricsApiTests(TestCase):
    """Test the authorized user tertiary_metrics API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@psmware.io',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tertiary_metrics(self):
        """Test retrieving tertiary_metrics"""
        TertiaryMetric.objects.create(
            user=self.user, metric='Architectural Stability')
        TertiaryMetric.objects.create(user=self.user, metric='Tooling')

        res = self.client.get(PRIMARY_METRIC_URL)

        tertiary_metrics = TertiaryMetric.objects.all().order_by('-metric')
        serializer = TertiaryMetricSerializer(tertiary_metrics, many=True)
        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_tertiary_metric_successful(self):
        """Test creating a new tertiary_metric"""
        payload = {'metric': 'Tooling'}
        self.client.post(PRIMARY_METRIC_URL, payload)

        exists = TertiaryMetric.objects.filter(
            user=self.user,
            metric=payload['metric']
        ).exists()
        # Assertion
        self.assertTrue(exists)

    def test_create_tertiary_metric_invalid(self):
        """Test creating a new tertiary_metric with invalid payload"""
        payload = {'metric': ''}
        res = self.client.post(PRIMARY_METRIC_URL, payload)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
