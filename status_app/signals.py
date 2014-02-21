import django.dispatch

request_signal = django.dispatch.Signal(providing_args=['path_info','request_time', 'status_code'])
