def nested_set(_obj, _keys, _value):
    for key in _keys[:-1]:
        _obj = _obj.setdefault(key, {})
    _obj[_keys[-1]] = _value

def nested_get(_obj, _keys):
    nobj = _obj
    for key in _keys:
        nobj = nobj.get(key)
        if not nobj: return None
    return nobj
