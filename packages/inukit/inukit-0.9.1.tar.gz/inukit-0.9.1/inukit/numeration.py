#给一个int 将其转换为radix进制数的形式并返回str
def num(inp: int, radix: int) -> str:
    if radix < 0 or radix > 36: 
        raise ValueError('Radix should be in [2, 36]')
    E = '0123456789abcdefghijklmnopqrstuvwxyz'
    tmp = ''
    d = inp
    while True:
        n = d % radix
        d = d // radix
        tmp = E[n] + tmp
        if d == 0:
            break
    return tmp

if __name__ == '__main__':
    print(num(114514, 2), bin(114514))
    print(num(114514, 8), oct(114514))
    print(num(114514, 16), hex(114514))
    print(i := num(114514, 3), int(i, 3))