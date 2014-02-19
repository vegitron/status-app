from django.core.management.base import NoArgsCommand
from django.utils import timezone
from datetime import timedelta
from status_app.dispatcher.model import dispatch
from random import random
from status_app.models import RawEvent

THREE_HOURS = 3 * 60
ITERATIONS = 1

class Command(NoArgsCommand):
    def handle_noargs(self, **kwargs):
        for i in range(THREE_HOURS):
            print "Minute %s of %s" % (i+1, THREE_HOURS)
            time = timezone.now() - timedelta(minutes = i)

            for j in range(ITERATIONS):
                pass_fail = True
                if random() < 0.1:
                    pass_fail = False

                dispatch('demo_data_pass_fail', RawEvent.PASS_FAIL, time, pass_fail, '', 'demo_host')

                time_random = random()
                time_value = 0.5
                if time_random > 0:
                    time_value = 1 / time_random

                dispatch('demo_data_interval', RawEvent.INTERVAL, time, time_value, '', 'demo_host')
