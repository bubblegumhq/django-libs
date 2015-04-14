def safe_int(i):
    try:
        return int(i)
    except (ValueError,TypeError):
        return None