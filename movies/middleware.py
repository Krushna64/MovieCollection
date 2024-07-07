import threading

class RequestCounterMiddleware:
    _lock = threading.Lock()
    _request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with self._lock:
            RequestCounterMiddleware._request_count += 1
        response = self.get_response(request)
        return response

    @classmethod
    def get_request_count(cls):
        with cls._lock:
            return cls._request_count

    @classmethod
    def reset_request_count(cls):
        with cls._lock:
            cls._request_count = 0
