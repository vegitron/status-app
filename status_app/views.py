from django.shortcuts import render_to_response
from status_app.models import EventBucket
from django.utils import timezone
from django import template
from datetime import datetime, timedelta

SIX_HOURS = 60 * 6

def status(request):
    starttime = timezone.now() + timedelta(hours=-6)

    event_buckets = EventBucket.objects.filter(bucket_type = EventBucket.MINUTE,
                        host=EventBucket.ALL_HOST_BUCKET,
                        start_time__gte = starttime)

    by_source = {}
    for bucket in event_buckets:
        if not bucket.source in by_source:
            by_source[bucket.source] = {}

        time = bucket.start_time.strftime("%H:%M")
        by_source[bucket.source][time] = bucket.display_count()

    display_data = []

    for bucket in by_source:
        minutes = []

        for i in range(SIX_HOURS):
            time = (starttime + timedelta(minutes = i)).strftime("%H:%M")
            if time in by_source[bucket]:
                minutes.append(by_source[bucket][time])
            else:
                minutes.append(0)


        display_data.append({
            "name": bucket,
            "minutes": minutes,
        })

    context = { "data": display_data }

    try:
        template.loader.get_template("status_app/status_wrapper.html")
        context['wrapper_template'] = 'status_app/status_wrapper.html'
    except template.TemplateDoesNotExist:
        context['wrapper_template'] = 'status_wrapper.html'
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass


    return render_to_response("app_status.html", context)

