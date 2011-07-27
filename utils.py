def process_getter(q_getter):
    # too clever? not clever enough?
    _module, _method = q_getter.rsplit('.', 1)
    module = __import__(_module, globals(), locals(), [_method], -1)
    return getattr(module, _method)
