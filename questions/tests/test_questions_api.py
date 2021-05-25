from questions.serializers import QuestionSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Question, PrimaryMetric, \
    SecondaryMetric, TertiaryMetric


QUESTION_URL = reverse('questions:question-list')


def sample_primary(user, metric='Test Primary Metric'):
    """Create and return a sample primary metric"""
    return PrimaryMetric.objects.create(user=user, metric=metric)


def sample_secondary(user, metric='Test Secondary Metric'):
    """Create and return a sample secondary metric"""
    return SecondaryMetric.objects.create(user=user, metric=metric)


def sample_tertiary(user, metric='Test Tertiary Metric'):
    """Create and return a sample tertiary metric"""
    return TertiaryMetric.objects.create(user=user, metric=metric)


def set_up_test_question(user,
                         primary_str='First',
                         secondary_str='Second',
                         tertiary_str='Third'):

    # create the primary metric
    primary = sample_primary(user, primary_str)
    #  create the secondary metric
    secondary = sample_secondary(user, secondary_str)
    #  create the tertiary metric
    tertiary = sample_tertiary(user, tertiary_str)
    # create the question
    Question.objects.create(
        user=user,
        primary_metric=primary,
        secondary_metric=secondary,
        tertiary_metric=tertiary
    )


class PublicQuestionsApiTests(TestCase):
    """Test the publicly available questions API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving questions"""
        res = self.client.get(QUESTION_URL)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateQuestionsApiTests(TestCase):
    """Test the authorized user questions API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@psmware.io',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.primary = sample_primary(self.user, 'Test Primary Metric')
        self.secondary = sample_secondary(self.user, 'Test Secondary Metric')
        self.tertiary = sample_tertiary(self.user, 'Test Tertiary Metric')

    def test_retrieve_questions(self):
        """Test retrieving questions"""
        set_up_test_question(user=self.user,
                             primary_str='Primary A',
                             secondary_str='Secondary A',
                             tertiary_str='Tertiary A')
        set_up_test_question(user=self.user,
                             primary_str='Primary B',
                             secondary_str='Secondary B',
                             tertiary_str='Tertiary B')

        res = self.client.get(QUESTION_URL)

        questions = Question.objects.all().order_by('id')
        serializer = QuestionSerializer(questions, many=True)
        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_question_successful(self):
        payload = {'primary_metric': self.primary.id,
                   'secondary_metric': self.secondary.id,
                   'tertiary_metric': self.tertiary.id}
        res = self.client.post(QUESTION_URL, payload)
        # Assertions
        # Verify question has been created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        question = Question.objects.get(id=res.data['id'])
        # Verify self.primary = question.primary
        primary = question.primary_metric
        self.assertEqual(primary, self.primary)
        # Verify self.secondary = question.secondary
        secondary = question.secondary_metric
        self.assertEqual(secondary, self.secondary)
        # Verify self.tertiary = question.tertiary
        tertiary = question.tertiary_metric
        self.assertEqual(tertiary, self.tertiary)

    def test_create_question_invalid(self):
        """Test creating a new question with invalid payload"""
        payload = {'primary_metric': '',
                   'secondary_metric': self.secondary.id,
                   'tertiary_metric': self.tertiary.id}
        res = self.client.post(QUESTION_URL, payload)
        # Assertion
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
