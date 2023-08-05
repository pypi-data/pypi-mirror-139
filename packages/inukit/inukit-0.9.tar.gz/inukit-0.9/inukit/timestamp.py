import time

def timestamp_now() -> int:
    return int(time.mktime(time.localtime()))

def timestamp(
    string: str,
    form: str = '%Y-%m-%d %H:%M:%S'
) -> int:
    return int(time.mktime(time.strptime(string, form)))

def natural_date(
    timestamp: int, 
    form: str = '%Y-%m-%d %H:%M:%S'
) -> str:
    if timestamp < 0:
        return None
    res = time.localtime(int(timestamp))
    return time.strftime(form, res)

def date_now(form: str = '%Y-%m-%d %H:%M:%S'):
    return natural_date(timestamp_now(), form)

def natural_time(timestamp: int) -> str:
    s = timestamp % 60
    m = (timestamp % 3600) // 60
    h = timestamp // 3600
    return f'{h} h {m} m {s} s'

if __name__ == '__main__':
    print(timestamp_now())
    print(date_now('%m-%d-%Y %H:%M:%S'))
    print(timestamp('2016-03-12 08:00:00'))
    print(natural_date(1457740800, '%Y-%m-%d'))
    print(natural_time(timestamp('2020-03-12 14:15:16') - timestamp('2016-05-20 22:32:12')))