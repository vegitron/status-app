"""
An interface for receivers to use, that will dispatch to values in settings
"""

from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

loaded_dispatchers = {}

def dispatch(source, event_type, timestamp, value, private_detail, host):
    dispatch_modules = getattr(settings, 'STATUS_APP_DISPATCHERS', [ 'status_app.dispatcher.model.dispatch' ])

    for module in list(set(dispatch_modules)):
        if not module in loaded_dispatchers:
            load_module(module)

        loaded_dispatchers[module](source, event_type, timestamp, value, private_detail, host)


def load_module(name):
    # This is all taken from django's static file finder
    module, attr = name.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))

    try:
        dispatch_function = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a '
                           '"%s" function' % (module, attr))

    loaded_dispatchers[name] = dispatch_function

