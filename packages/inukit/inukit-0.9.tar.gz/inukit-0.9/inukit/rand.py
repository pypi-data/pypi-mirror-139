import random

def rand_a_int(a: int, b: int) -> int:
    return random.randint(a, b)

def rand_some_int(a: int, b: int, amount: int) -> tuple:
    res = []
    for i in range(0, amount):
        tmp = rand_a_int(a, b)
        res.append(tmp)
    return tuple(res)

def rand_bool() -> bool:
    return bool(rand_a_int(0,1))