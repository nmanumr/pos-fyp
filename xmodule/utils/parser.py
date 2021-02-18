def parse_int(value, default=None):
    if value and value.isdigit():
        return int(value)

    return default


def parse_bool(value, default=None):
    if not value:
        return default

    value = value.lower()
    if value in ['1', 't', 'true']:
        return True

    elif value in ['0', 'f', 'false']:
        return False

    return default
