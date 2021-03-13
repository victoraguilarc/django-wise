

def clean_boolean(item=None):
    """Parse string boolean values."""
    if item is not None:
        if isinstance(item, str):
            return item.lower() == 'true'
        elif isinstance(item, bool):
            return item
    return False
