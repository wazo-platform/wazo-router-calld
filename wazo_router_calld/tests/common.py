from wazo_router_calld.worker import WazoRouterCalld

from functools import wraps


def get_worker(f):
    @wraps(f)
    def wrapper(*args, **kw):
        context = dict(
            api_uri="http://localhost:8000",
            messagebus_uri="pyamqp://wazo:wazo@localhost:5672//",
        )
        worker = WazoRouterCalld(context=context)
        return f(*args, worker=worker)

    return wrapper
