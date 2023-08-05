import base64
from . import numeration as n

_d = {
    '嗷': '0',
    '呜': '1',
    '汪': '2'
}
_e = {
    '0': '嗷',
    '1': '呜',
    '2': '汪'
}

#将字符串加密为狗语
def enc(inp: str) -> str:
    tmp = inp.encode(encoding='utf-8')
    tmp = base64.b16encode(tmp)
    tmp = int(tmp, 16)
    tmp = n.num(tmp, 3)
    tmp = ''.join([_e[each] for each in tmp])
    return tmp

#狗语解密
def dec(inp: str) -> str:
    tmp = ''.join([_d[each] for each in inp])
    tmp = int(tmp, 3)
    tmp = hex(tmp)[2:].upper()
    tmp = base64.b16decode(tmp)
    tmp = tmp.decode(encoding='utf-8')
    return tmp