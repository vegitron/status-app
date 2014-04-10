from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django import template
from datetime import datetime, timedelta
from status_app import datasource

def status(request):
    starttime = timezone.now() + timedelta(hours=-6)

    display_data = datasource.get_aggregate_data(starttime)

    context = { "data": display_data }

    try:
        template.loader.get_template("status_app/status_wrapper.html")
        context['wrapper_template'] = 'status_app/status_wrapper.html'
    except template.TemplateDoesNotExist:
        context['wrapper_template'] = 'status_wrapper.html'
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass

    return render_to_response("app_status.html", context, context_instance=RequestContext(request))

