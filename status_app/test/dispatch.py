from django.test import TestCase
from status_app.models import EventBucket, RawEvent
from status_app.dispatcher.memory import get_all_events, clear_all_events
from status_app.dispatch import dispatch
from django.utils import timezone

class DispatchTest(TestCase):

    def test_valid_settings(self):
        with self.settings(STATUS_APP_DISPATCHERS= ['status_app.dispatcher.memory.dispatch']):
            clear_all_events()
            dispatch('dt_test_settings', RawEvent.PASS_FAIL, timezone.now(), True, '', 'test')

            all_events = get_all_events()
            self.assertEquals(len(all_events), 1)
            self.assertEquals(all_events[0][0], 'dt_test_settings')

    def test_double_settings(self):
        with self.settings(STATUS_APP_DISPATCHERS= ['status_app.dispatcher.memory.dispatch', 'status_app.dispatcher.memory.dispatch']):
            clear_all_events()
            dispatch('dt_test_settings', RawEvent.PASS_FAIL, timezone.now(), True, '', 'test')

            all_events = get_all_events()
            self.assertEquals(len(all_events), 1)
            self.assertEquals(all_events[0][0], 'dt_test_settings')

    def test_second_setting(self):
        with self.settings(STATUS_APP_DISPATCHERS= ['status_app.dispatcher.model.dispatch', 'status_app.dispatcher.memory.dispatch']):
            clear_all_events()
            dispatch('dt_test_settings', RawEvent.PASS_FAIL, timezone.now(), True, '', 'test')

            all_events = get_all_events()
            self.assertEquals(len(all_events), 1)
            self.assertEquals(all_events[0][0], 'dt_test_settings')

