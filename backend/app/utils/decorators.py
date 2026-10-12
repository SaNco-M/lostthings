import time
from functools import wraps

from backend.app.models import AdminModel


def time_logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(end_time - start_time)
        return res

    return wrapper


def type_check(**expected_types):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for kwarg in kwargs:
                if kwarg in expected_types:
                    if not isinstance(kwargs[kwarg], expected_types[kwarg]):
                        raise TypeError("Неверный тип данных")

            res = func(*args, **kwargs)

            return res

        return wrapper

    return real_decorator


def admin_required(func):
    def wrapper(*args, **kwargs):
        initiator = args[1]

        if not isinstance(initiator, AdminModel):
            raise PermissionError("Доступ запрещен!")

        return func(*args, **kwargs)

    return wrapper
