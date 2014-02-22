from datetime import datetime
from status_app.signals import request_signal

class TimingMiddleware(object):
    _process_data = {}

    def process_request(self, request):
        # self is reused :(
        self._process_data = {}
        self._process_data['start_time'] = datetime.now()

        return None

    def process_response(self, request, response):
        now = datetime.now()

        start = self._process_data['start_time']

        seconds_taken = (now - start).total_seconds()

        request_signal.send(sender=self,
                            path_info = request.path_info,
                            request_time = seconds_taken,
                            status_code = response.status_code)
        return response
