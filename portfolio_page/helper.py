import os
import pickle
import requests
import flask
from typing import Union, Callable, Any, get_type_hints

CACHE_DIRECTORY = "cache"


def returns_str(func):
    return get_type_hints(func)['return'] is str


def persist_result(func, path, result):
    if result is None:
        return

    if returns_str(func):
        with open(path, 'w+') as f:
            f.write(str(result))
    else:
        with open(path, 'wb+') as f:
            pickle.dump(result, f)


def load_result(func, path):
    if returns_str(func):
        with open(path) as f:
            return f.read()
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)


def cache(path_or_path_func: Union[str, Callable[[Any], str]]):
    """
    This decorator caches the result of a function in a file.
    The decorated function is only executed the very first time.
    Any further calls will return the cached result.
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            if not os.path.exists(CACHE_DIRECTORY):
                os.mkdir(CACHE_DIRECTORY)

            path = path_or_path_func
            if callable(path_or_path_func):
                path = path_or_path_func(*args, **kwargs)

            path = os.path.join(CACHE_DIRECTORY, path)
            if not os.path.exists(path):
                result = func(*args, **kwargs)
                persist_result(func, path, result)
            else:
                result = load_result(func, path)

            return result
        return inner
    return wrapper


def report_error(r: requests.Response):
    flask.current_app.logger.error(
        'Failed request (%d): "%s"', r.status_code, r.text)
