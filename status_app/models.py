from django.db import models

class RawEvent(models.Model):
    PASS_FAIL = 0
    INTERVAL = 1
    TEXT = 2

    EVENT_TYPE_CHOICES = (
        (PASS_FAIL, "Pass/Fail"),
        (INTERVAL, "Time taken"),
        (TEXT, "Text value"),
    )

    source = models.CharField(max_length=100, db_index=True)
    event_type = models.IntegerField(choices=EVENT_TYPE_CHOICES)
    timestamp = models.DateTimeField(db_index=True)
    value = models.CharField(max_length=100)
    private_detail = models.TextField()
    host = models.CharField(max_length=200, db_index=True)


class EventBucket(models.Model):
    """ Stored aggregated data, for quick display """
    ALL_HOST_BUCKET = "*"

    MINUTE = 0
    HOUR = 1
    DAY = 2

    BUCKET_TYPE_CHOICES = (
        (MINUTE, "minute"),
        (HOUR, "hour"),
        (DAY, "day"),
    )

    source = models.CharField(max_length=100, db_index=True)
    host = models.CharField(max_length=200, db_index=True)
    event_type = models.IntegerField(choices=RawEvent.EVENT_TYPE_CHOICES)

    bucket_type = models.IntegerField(choices=BUCKET_TYPE_CHOICES)
    start_time = models.DateTimeField(db_index=True)

    # For pass/fail and interval, to get averages
    total_count = models.IntegerField()

    # For pass/fail events:
    total_pass = models.IntegerField()

    # For interval events:
    total_time = models.FloatField()

    # For text events:
    unique_values = models.IntegerField()


    class Meta:
        unique_together = ('source', 'host', 'event_type', 'bucket_type', 'start_time')
