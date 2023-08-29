import re

class Config:

    def __init__(self):
        self.data = {}
        with open('.env') as f:
            pattern = r"^(?P<key>[^=]+)=(?P<value>.*)"
            for line in f.readlines():
                m = re.match(pattern, line)
                if m:
                    key = m.group('key')
                    value = m.group('value')
                    if key:
                        self.data[key] = value

    def get(self, key):
        return self.data.get(key, None)
