from datetime import datetime, timedelta
from status_app.models import EventBucket, RawEvent
from status_app.dispatcher.memory import sources, by_minute

SIX_HOURS = 60 * 6 + 1

def get_aggregate_data(starttime):
    starttime = starttime.replace(second=0, microsecond=0)
    dummy_event = EventBucket()
    display_data = []
    for source in sources:
        minutes = []

        for i in range(SIX_HOURS):
            time_str = (starttime + timedelta(minutes = i)).isoformat(' ')

            if time_str in by_minute[source]:
                data = by_minute[source][time_str]
                dummy_event.total_count = data['total_count']
                dummy_event.total_pass = data['total_pass']
                dummy_event.total_time = data['total_time']
                dummy_event.unique_values  = 0
                dummy_event.event_type = sources[source]
                value = dummy_event.display_count()

                minutes.append(value)
            else:
                value = 0
                minutes.append(value)


        bucket_data = {
            "name": source,
            "minutes": minutes,
        }

        if sources[source] == RawEvent.PASS_FAIL:
            bucket_data['pass_fail'] = True

        elif sources[source] == RawEvent.INTERVAL:
            bucket_data['interval'] = True

        elif sources[source] == RawEvent.TEXT:
            bucket_data['text'] = True

        display_data.append(bucket_data)


    return display_data
