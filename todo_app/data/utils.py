from typing import Any, Callable

import requests

from todo_app.data.exceptions import ResponseError


def catch_response_failure(func: Callable[[Any], requests.Response]):
    def wrap(*args, **kwargs):
        r = func(*args, **kwargs)
        if not r.ok:
            raise ResponseError
        return r

    return wrap
