import json
import os

class JsonData:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            self.writes('')

    def reads(self) -> str:
        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()
        return data

    def writes(self, to_write: str):
        with open(self.path, 'w+', encoding='utf-8') as f:
            f.write(to_write)

    def gets(self, keys: tuple):
        tmp = self.read()
        for each in keys:
            if isinstance(tmp, dict):
                tmp = tmp.get(each)
            else:
                return None
        return tmp
    
    #这个函数全都是魔法 我也不知道我写的啥 但是能跑而且跑得好像还行
    def sets(self, keys: tuple, value):
        data = self.read()
        for i in range(1, len(keys)+1):
            s = keys[0:i]
            loc = ''.join([f'[\'{x}\']' for x in s])
            loc = f'data{loc}'
            try:
                tmp = eval(loc)
            except KeyError:
                tmp = None
            if i == len(keys):
                exec(f'{loc} = value')
                break
            elif not isinstance(tmp, dict):
                exec(f'{loc} = ' + '{}')
        self.write(data)
    
    def read(self) -> object:
        data_str = self.reads()
        if data_str == '':
            data_str = '{}'
            self.writes(data_str)
        return json.loads(data_str)

    def write(self, to_write: object):
        return self.writes(json.dumps(to_write, indent=4))
    
    def get(self, key: str):
        keys = key.split('.')
        return self.gets(keys)

    def set(self, key: str, value):
        keys = key.split('.')
        return self.sets(keys, value)

    def __str__(self):
        return self.reads()

if __name__ == '__main__':
    jconf = JsonData('src/conf.json')
    jconf.set('settings.port', 3389)
    port = jconf.get('settings.port')