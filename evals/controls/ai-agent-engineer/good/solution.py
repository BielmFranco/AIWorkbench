def resolve(provider, key, max_attempts):
    if max_attempts <= 0: raise ValueError('budget must be positive')
    used = 1
    try:
        state = provider.refund(key)
    except TimeoutError:
        state = 'pending'
    while state == 'pending' and used < max_attempts:
        state = provider.lookup(key)
        used += 1
    return state if state in ('issued','denied') else 'unresolved'
