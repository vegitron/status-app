from django.test import TestCase
from status_app.dispatcher.memory import get_all_events, clear_all_events
from status_app.receiver_initialization import load_receivers
from django.core.exceptions import ImproperlyConfigured
from django.test.client import Client
import contextlib

class ReceiverTest(TestCase):

    def test_valid_settings(self):
        with self.settings(STATUS_APP_RECEIVERS= ['status_app.receiver.sample_receiver']):
            try:
                load_receivers()
            except ImproperlyConfigured:
                self.fail('Could not load sample_receiver')

    def test_invalid_settings(self):
        with contextlib.nested(self.settings(STATUS_APP_RECEIVERS=['status_app.receiver.missing_receiver']),
                               self.assertRaises(ImproperlyConfigured)):
            load_receivers()

    def test_request(self):
        with contextlib.nested(self.settings(STATUS_APP_RECEIVERS=['status_app.receiver.sample_receiver']),
                               self.settings(STATUS_APP_DISPATCHERS=['status_app.dispatcher.memory.dispatch'])):
            clear_all_events()
            load_receivers()

            c = Client()
            c.get('/status')
            all_events = get_all_events()

            self.assertEquals(len(all_events), 1)
            self.assertEquals(all_events[0][0], 'test_request_finished')