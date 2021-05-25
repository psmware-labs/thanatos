from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import SecondaryMetric

from metrics.serializers import SecondaryMetricSerializer


SECONDARY_METRIC_URL = reverse('metrics:secondarymetric-list')


class PublicSecondaryMetricsApiTests(TestCase):
    """Test the publicly available secondary_metrics API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving secondary_metrics"""
        res = self.client.get(SECONDARY_METRIC_URL)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSecondaryMetricsApiTests(TestCase):
    """Test the authorized user secondary_metrics API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@psmware.io',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_secondary_metrics(self):
        """Test retrieving secondary_metrics"""
        SecondaryMetric.objects.create(
            user=self.user, metric='Architectural Stability')
        SecondaryMetric.objects.create(user=self.user, metric='Tooling')

        res = self.client.get(SECONDARY_METRIC_URL)

        secondary_metrics = SecondaryMetric.objects.all().order_by('-metric')
        serializer = SecondaryMetricSerializer(secondary_metrics, many=True)
        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_secondary_metric_successful(self):
        """Test creating a new secondary_metric"""
        payload = {'metric': 'Tooling'}
        self.client.post(SECONDARY_METRIC_URL, payload)

        exists = SecondaryMetric.objects.filter(
            user=self.user,
            metric=payload['metric']
        ).exists()
        # Assertion
        self.assertTrue(exists)

    def test_create_secondary_metric_invalid(self):
        """Test creating a new secondary_metric with invalid payload"""
        payload = {'metric': ''}
        res = self.client.post(SECONDARY_METRIC_URL, payload)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
