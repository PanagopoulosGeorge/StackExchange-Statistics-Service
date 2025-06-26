import time
import functools
from threading import Lock
'''
from functools import wraps
def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')
example()
'Calling decorated function'
'Called example function'
'''
def rate_limited(max_per_second):

    """A decorator to limit the rate of function calls 
    to `max_per_second`."""

    min_interval = 1.0 / max_per_second
    lock = Lock()
    def decorator(func):
        last_called = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                elapsed = time.time() - last_called[0]
                wait = min_interval - elapsed
                if wait > 0:
                    time.sleep(wait)
                result = func(*args, **kwargs)
                last_called[0] = time.time()
                return result
        return wrapper
    return decorator


def throttle_backoff_limited(func):
    last_called = [0.0]
    lock = Lock()
    throttle = [0.0]
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            elapsed = time.time() - last_called[0]
            wait = throttle[0] - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            if 'backoff' in result:
                throttle[0] = result['backoff']
            else:
                throttle[0] = 0.0
            last_called[0] = time.time()
            return result
    return wrapper
