

def clean_boolean(item=None):
    if item is not None:
        if isinstance(item, str):
            return True if item == 'true' else False
        elif isinstance(item, bool):
            return item
    return False
