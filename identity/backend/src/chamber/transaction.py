from functools import wraps


def transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except OptimisticLockFailed:
                continue

    return wrapper


class OptimisticLockFailed(Exception):
    pass
