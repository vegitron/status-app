from django.utils.importlib import import_module
from django.conf import settings

def get_aggregate_data(starttime):
    ds_module = getattr(settings, 'STATUS_APP_DATASOURCE', 'status_app.datasource.memory')
    mod = import_module(ds_module)

    return mod.get_aggregate_data(starttime)

