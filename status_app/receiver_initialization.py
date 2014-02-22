from django.conf import settings
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

# Get a settings value for receivers, with some smart default.
# initialize each module, so they start actually receiving signals

loaded_receivers = {}
loaded_signals = {}

def load_receivers():
    receivers = getattr(settings, 'STATUS_APP_RECEIVERS', [])
    for module in list(set(receivers)):
        if not module in loaded_receivers:
            load_module(module)

        loaded_signals[module].connect(loaded_receivers[module])


def load_module(name):
    # This is all taken from django's static file finder
    module, attr = name.rsplit('.', 1)
    try:
        receiver_module = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))

    try:
        receiver_function = getattr(receiver_module, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a '
                           '"%s" function' % (module, attr))

    try:
        signal = receiver_module.get_signal()
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"get_signal" function' % module)

    loaded_receivers[name] = receiver_function
    loaded_signals[name] = signal

