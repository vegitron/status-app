from django.test import TestCase
from status_app.dispatcher.model import dispatch
from status_app.models import EventBucket, RawEvent
from django.utils import timezone

class PassFailTest(TestCase):
    def test_one_pass(self):
        dispatch('pft_test_one_pass', RawEvent.PASS_FAIL, timezone.now(), True, '', 'test')

    def test_aggregate(self):
        now = timezone.now()
        dispatch('pft_test_aggregate', RawEvent.PASS_FAIL, now, True, '', 'test1')
        dispatch('pft_test_aggregate', RawEvent.PASS_FAIL, now, True, '', 'test2')
        dispatch('pft_test_aggregate', RawEvent.PASS_FAIL, now, True, '', 'test1')
        dispatch('pft_test_aggregate', RawEvent.PASS_FAIL, now, False, '', 'test2')
        dispatch('pft_test_aggregate', RawEvent.PASS_FAIL, now, False, '', 'test1')

        bucket = EventBucket.objects.get(source='pft_test_aggregate', bucket_type=EventBucket.MINUTE, host=EventBucket.ALL_HOST_BUCKET)

        self.assertTrue(bucket.total_count, 5)
        self.assertTrue(bucket.total_pass, 3)

        bucket = EventBucket.objects.get(source='pft_test_aggregate', bucket_type=EventBucket.MINUTE, host='test1')
        self.assertTrue(bucket.total_count, 3)
        self.assertTrue(bucket.total_pass, 2)

        bucket = EventBucket.objects.get(source='pft_test_aggregate', bucket_type=EventBucket.MINUTE, host='test2')
        self.assertTrue(bucket.total_count, 2)
        self.assertTrue(bucket.total_pass, 1)

class IntervalTest(TestCase):
    def test_one_pass(self):
        dispatch('it_test_one_pass', RawEvent.INTERVAL, timezone.now(), 13.2, '', 'test')

    def test_aggregate(self):
        now = timezone.now()
        dispatch('it_test_aggregate', RawEvent.INTERVAL, now, 1.5, '', 'test1')
        dispatch('it_test_aggregate', RawEvent.INTERVAL, now, 1.5, '', 'test2')
        dispatch('it_test_aggregate', RawEvent.INTERVAL, now, 2.0, '', 'test1')
        dispatch('it_test_aggregate', RawEvent.INTERVAL, now, 2.0, '', 'test2')
        dispatch('it_test_aggregate', RawEvent.INTERVAL, now, 5.0, '', 'test1')

        bucket = EventBucket.objects.get(source='it_test_aggregate', bucket_type=EventBucket.MINUTE, host=EventBucket.ALL_HOST_BUCKET)

        self.assertTrue(bucket.total_count, 5)
        self.assertTrue(bucket.total_time, 12.0)

        bucket = EventBucket.objects.get(source='it_test_aggregate', bucket_type=EventBucket.MINUTE, host='test1')
        self.assertTrue(bucket.total_count, 3)
        self.assertTrue(bucket.total_time, 8.5)

        bucket = EventBucket.objects.get(source='it_test_aggregate', bucket_type=EventBucket.MINUTE, host='test2')
        self.assertTrue(bucket.total_count, 2)
        self.assertTrue(bucket.total_time, 3.5)


class ValueTest(TestCase):
    def test_one_pass(self):
        dispatch('vt_test_one_pass', RawEvent.TEXT, timezone.now(), 'ok', '', 'test')

    def test_aggregate(self):
        now = timezone.now()
        dispatch('vt_test_aggregate', RawEvent.TEXT, now, 'pmichaud', '', 'test1')
        dispatch('vt_test_aggregate', RawEvent.TEXT, now, 'vegitron', '', 'test2')
        dispatch('vt_test_aggregate', RawEvent.TEXT, now, 'vegitron', '', 'test1')
        dispatch('vt_test_aggregate', RawEvent.TEXT, now, 'vegitron1', '', 'test2')
        dispatch('vt_test_aggregate', RawEvent.TEXT, now, 'vegitron2', '', 'test1')

        bucket = EventBucket.objects.get(source='vt_test_aggregate', bucket_type=EventBucket.MINUTE, host=EventBucket.ALL_HOST_BUCKET)
        self.assertTrue(bucket.unique_values, 4)

        bucket = EventBucket.objects.get(source='vt_test_aggregate', bucket_type=EventBucket.MINUTE, host='test1')
        self.assertTrue(bucket.unique_values, 3)

        bucket = EventBucket.objects.get(source='vt_test_aggregate', bucket_type=EventBucket.MINUTE, host='test2')
        self.assertTrue(bucket.unique_values, 2)

