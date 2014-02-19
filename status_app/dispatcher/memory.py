
all_events = []
def dispatch(source, event_type, timestamp, value, private_detail, host):
    all_events.append([source, event_type, timestamp, value, private_detail, host])

def get_all_events():
    return all_events

def clear_all_events():
    del all_events[:]

