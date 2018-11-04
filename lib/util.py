import math


class Parser:
    def __init__(self, path, separator='=', escape='"'):
        self.path = path
        self.separator = separator
        self.escape = escape
        with open(path) as f:
            self.file = f.readlines()

    def readall(self):
        for line in self.file:
            pos = 0
            for ch in line:
                if ch == ' ' or ch == '\n':
                    print('xd')
