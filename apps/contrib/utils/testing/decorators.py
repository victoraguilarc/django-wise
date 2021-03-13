from contextlib import contextmanager


@contextmanager
def temporarily(obj, **kwargs):
    """Set attributes to a model, temorally."""
    original_values = {key: getattr(obj, key) for key in kwargs}
    for key1, value1 in kwargs.items():
        setattr(obj, key1, value1)

    obj.save(update_fields=kwargs.keys())

    try:
        yield

    finally:
        for key2, value2 in original_values.items():
            setattr(obj, key2, value2)
        obj.save(update_fields=original_values.keys())
