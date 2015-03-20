def safe_int(i):
    try:
        return int(i)
    except TypeError:
        return None