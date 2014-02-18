from django.test import TestCase
from status_app.dispatcher.model import dispatch
from status_app.models import EventBucket, RawEvent
from django.utils import timezone

class PassFailTest(TestCase):
    def test_one_pass(self):
        dispatch('pft_test_one_pass', RawEvent.PASS_FAIL, timezone.now(), True, '', 'test')


class IntervalTest(TestCase):
    def test_one_pass(self):
        dispatch('it_test_one_pass', RawEvent.INTERVAL, timezone.now(), 13.2, '', 'test')


class ValueTest(TestCase):
    def test_one_pass(self):
        dispatch('vt_test_one_pass', RawEvent.TEXT, timezone.now(), 'ok', '', 'test')

