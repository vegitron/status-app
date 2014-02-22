from datetime import datetime, timedelta
from status_app.models import EventBucket, RawEvent

SIX_HOURS = 60 * 6

def get_aggregate_data(starttime):
    event_buckets = EventBucket.objects.filter(bucket_type = EventBucket.MINUTE,
                        host=EventBucket.ALL_HOST_BUCKET,
                        start_time__gte = starttime)

    by_source = {}
    for bucket in event_buckets:
        if not bucket.source in by_source:
            by_source[bucket.source] = {}

        time = bucket.start_time.strftime("%H:%M")
        by_source[bucket.source][time] = bucket.display_count()
        by_source[bucket.source]['bucket'] = bucket

    display_data = []

    for bucket in by_source:
        minutes = []

        for i in range(SIX_HOURS):
            time = (starttime + timedelta(minutes = i)).strftime("%H:%M")
            if time in by_source[bucket]:
                minutes.append(by_source[bucket][time])
            else:
                minutes.append(0)

        bucket_data = {
            "name": bucket,
            "minutes": minutes,
        }

        bucket_obj = by_source[bucket]['bucket']
        if bucket_obj.event_type == RawEvent.PASS_FAIL:
            bucket_data['pass_fail'] = True

        elif bucket_obj.event_type == RawEvent.INTERVAL:
            bucket_data['interval'] = True

        elif bucket_obj.event_type == RawEvent.TEXT:
            bucket_data['text'] = True

        display_data.append(bucket_data)

    return display_data
