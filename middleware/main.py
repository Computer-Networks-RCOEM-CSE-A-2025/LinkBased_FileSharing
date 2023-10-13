from typing import Any


class TokenMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request,*args: Any, **kwds: Any) -> Any:
        try:
            response = self.get_response(request)
            print("********* Middleware called with request ********",request.data)
            return response
        except:
            response = self.get_response(request)
            print("********* Middleware called ********")
            return response
