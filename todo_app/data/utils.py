from functools import wraps
from typing import Any, Callable

import requests

from todo_app.data.exceptions import ResponseError


def catch_response_failure(func: Callable[[Any], requests.Response]):
    @wraps(func)
    def wrap(*args, **kwargs):
        r = func(*args, **kwargs)
        if not r.ok:
            raise ResponseError(r.json())
        return r

    return wrap
