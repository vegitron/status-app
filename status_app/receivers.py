from status_app.signals import request_signal
from status_app.dispatch import dispatch
from status_app.models import RawEvent
from django.dispatch import receiver
from datetime import datetime
import socket

@receiver(request_signal)
def request_receiver(sender, status_code, path_info, request_time, **kwargs):
    if status_code >= 200 and status_code < 400:
        dispatch('application_response', RawEvent.PASS_FAIL, datetime.now(), True, '', socket.gethostname())
    else:
        dispatch('application_response', RawEvent.PASS_FAIL, datetime.now(), False, path_info, socket.gethostname())


    dispatch('application_response_time', RawEvent.INTERVAL, datetime.now(), request_time, '', socket.gethostname())

    print "In a receiver: ", kwargs

