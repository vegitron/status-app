""" An event dispatcher that goes right into the model storage. """

from status_app.models import EventBucket, RawEvent
from django.db.models import Count
from datetime import timedelta

def dispatch(source, event_type, timestamp, value, private_detail, host):
    # XXX - assuming event_type is coming in as RawEvent.<foo> integer value
    RawEvent.objects.create(source=source, event_type=event_type,
                            timestamp=timestamp, value=value,
                            private_detail=private_detail, host=host)


    all_hosts = EventBucket.ALL_HOST_BUCKET
    timestamp = timestamp.replace(microsecond=0)
    minute_start = timestamp.replace(second=0)
    hour_start = timestamp.replace(second=0, minute=0)
    day_start = timestamp.replace(second=0, minute=0, hour=0)

    buckets = []
    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=host, event_type=event_type,
                            bucket_type=EventBucket.MINUTE,
                            start_time=minute_start)[0])

    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=all_hosts, event_type=event_type,
                            bucket_type=EventBucket.MINUTE,
                            start_time=minute_start)[0])

    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=host, event_type=event_type,
                            bucket_type=EventBucket.HOUR,
                            start_time=hour_start)[0])

    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=all_hosts, event_type=event_type,
                            bucket_type=EventBucket.HOUR,
                            start_time=hour_start)[0])

    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=host, event_type=event_type,
                            bucket_type=EventBucket.DAY,
                            start_time=day_start)[0])

    buckets.append(EventBucket.objects.get_or_create(source=source,
                            host=all_hosts, event_type=event_type,
                            bucket_type=EventBucket.DAY,
                            start_time=day_start)[0])

    for bucket in buckets:
        # I'd like this to be replaced with something like
        # UPDATE bucket set value = value + 1
        if RawEvent.PASS_FAIL == event_type:
            bucket.total_count = bucket.total_count + 1

            if value == True:
                bucket.total_pass = bucket.total_pass + 1

        elif RawEvent.INTERVAL == event_type:
            bucket.total_count = bucket.total_count + 1
            bucket.total_time = bucket.total_time + value

        elif RawEvent.TEXT == event_type:
            if EventBucket.MINUTE == bucket.bucket_type:
                start_time = minute_start
                end_time = start_time + timedelta(minutes=1)
            elif EventBucket.HOUR == bucket.bucket_type:
                start_time = hour_start
                end_time = start_time + timedelta(hours=1)
            elif EventBucket.DAY == bucket.bucket_type:
                start_time = day_start
                end_time = start_time + timedelta(days=1)

            # XXX - is there a more efficient way to get this?
            filter1 = RawEvent.objects.filter(source=bucket.source,
                                    event_type = bucket.event_type,
                                    timestamp__gte = start_time,
                                    timestamp__lt = end_time)

            if EventBucket.ALL_HOST_BUCKET != bucket.host:
                filtered = filter1.filter(host = bucket.host)

            else:
                filtered = filter1

            bucket.unique_values = filtered.aggregate(Count('value', distinct=True))["value__count"]

        bucket.save()



