from functools import wraps
from threading import Lock

lock = Lock()


def synchronized(lock):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)

        return wrapped

    return wrapper


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        cls._instance = None
        super().__init__(name, bases, attrs)

    @synchronized(lock)
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
