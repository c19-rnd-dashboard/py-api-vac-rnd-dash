def coalesce(*args, default=None):
    val = None
    if len(args) > 1:
        for arg in args:
            if arg is not None:
                val = arg
                break

    if default:
        if val is None:
            val = default

    return val
