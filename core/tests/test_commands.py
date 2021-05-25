from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    # Mocking the database call incase the database is not available
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # Building the mock object
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # configuring the mock object to be successful
            gi.return_value = True
            call_command('wait_for_db')
            # Assertion
            self.assertEqual(gi.call_count, 1)

    # Overriding the behavior of time.sleep
    # so that the test will not wait
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # The side effect will raise the error five times then will
            # return true on the sixth time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            # Assertion
            self.assertEqual(gi.call_count, 6)
