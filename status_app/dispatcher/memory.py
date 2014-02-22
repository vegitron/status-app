from status_app.models import RawEvent
from django.utils import timezone

all_events = []
by_minute = {}
sources = {}

def dispatch(source, event_type, timestamp, value, private_detail, host):
    all_events.append([source, event_type, timestamp, value, private_detail, host])

    sources[source] = event_type

    # Just do the same thing the frontend does :(
    timestamp = timezone.now()
    minute_start = timestamp.replace(second=0, microsecond=0)
    minute_str = minute_start.isoformat(' ')

    if source not in by_minute:
        by_minute[source] = {}

    if minute_str not in by_minute[source]:
        by_minute[source][minute_str] = {
                                        'total_count': 0,
                                        'total_pass': 0,
                                        'total_time': 0,
                                        }

    bucket = by_minute[source][minute_str]

    if RawEvent.PASS_FAIL == event_type:
        bucket['total_count'] = bucket['total_count'] + 1

        if value == True:
            bucket['total_pass'] = bucket['total_pass'] + 1

    elif RawEvent.INTERVAL == event_type:
        bucket['total_count'] = bucket['total_count'] + 1
        bucket['total_time'] = bucket['total_time'] + value

    elif RawEvent.TEXT == event_type:
        print "Not doing aggregations for TEXT yet"


def get_all_events():
    return all_events

def clear_all_events():
    del all_events[:]

