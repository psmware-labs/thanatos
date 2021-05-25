from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@psmware.io', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@psmware.io'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        # Assertions
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@PSMWARE.IO'
        user = get_user_model().objects.create_user(email, 'test123')
        # Assertion
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # Assertions
        # Here, if a value error is NOT raised, we have an error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'superuser@psmware.io',
            'test123'
        )
        # Assertions
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_account_str(self):
        """Test the Account string representation"""
        account = models.Account.objects.create(
            user=sample_user(),
            name='Raytheon'
        )
        # Assertion
        self.assertEqual(str(account), account.name)

    def test_primary_metric_str(self):
        """Test the Primary Metric string representation"""
        primary = models.PrimaryMetric.objects.create(
            user=sample_user(),
            metric='Architectural Stability'
        )
        # Assertion
        self.assertEqual(str(primary), primary.metric)

    def test_secondary_metric_str(self):
        """Test the Secondary Metric string representation"""
        secondary = models.SecondaryMetric.objects.create(
            user=sample_user(),
            metric='Access Control Standards applied'
        )
        # Assertion
        self.assertEqual(str(secondary), secondary.metric)

    def test_tertiary_metric_str(self):
        """Test the Tertiary Metric string representation"""
        tertiary = models.TertiaryMetric.objects.create(
            user=sample_user(),
            metric='ARB or Change Board convenes weekly'
        )
        # Assertion
        self.assertEqual(str(tertiary), tertiary.metric)

    def test_question_str(self):
        """Test the question string representation"""
        # setup up the user for this test
        question_user = sample_user()

        # create teh primary metric
        primary = models.PrimaryMetric.objects.create(
            user=question_user,
            metric='Primary'
        )

        #  create the secondary metric
        secondary = models.SecondaryMetric.objects.create(
            user=question_user,
            metric='Secondary'
        )

        #  create the tertiary metric
        tertiary = models.TertiaryMetric.objects.create(
            user=question_user,
            metric='Secondary'
        )

        # create the question
        question = models.Question.objects.create(
            user=question_user,
            primary_metric=primary,
            secondary_metric=secondary,
            tertiary_metric=tertiary
        )
        # Assertion
        self.assertEqual(str(question), primary.metric +
                         secondary.metric + tertiary.metric)
