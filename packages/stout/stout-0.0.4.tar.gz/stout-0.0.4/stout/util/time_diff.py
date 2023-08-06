from datetime import datetime

def time_diff(past, future, fmt='%Y-%m-%d', interval='days'):
    return ((
        future if type(future) == datetime else datetime.strptime(future, fmt)
    ) - (
        past if type(past) == datetime else datetime.strptime(past, fmt)
    )).__getattribute__(interval)