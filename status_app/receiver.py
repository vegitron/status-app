from status_app.dispatch import dispatch
from status_app.models import RawEvent
from django.utils import timezone
from django.core.signals import request_finished


def sample_receiver(sender, **kwargs):
    dispatch('test_request_finished', RawEvent.TEXT, timezone.now(), '', '', '')


def get_signal():
    return request_finished