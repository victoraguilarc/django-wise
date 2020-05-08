from contextlib import contextmanager


@contextmanager
def temporarily(obj, **kwargs):
    original_values = {k: getattr(obj, k) for k in kwargs}

    for k, v in kwargs.items():
        setattr(obj, k, v)

    obj.save(update_fields=kwargs.keys())

    try:
        yield

    finally:
        for k, v in original_values.items():
            setattr(obj, k, v)

        obj.save(update_fields=original_values.keys())
