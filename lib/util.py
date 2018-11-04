import math


class Parser:
    def __init__(self, path, escape='"'):
        self.path = path
        self.escape = escape
        with open(path) as f:
            self.file = f.readlines()

    def readall(self):
        ret = []
        for line in self.file:
            var = ''
            temp = 0
            inphr = True
            for ch in range(1, len(line)):
                if line[ch] == self.escape:
                    if inphr:
                        inphr = False
                        if temp == 0:
                            temp = var
                        else:
                            ret.append((temp, var))
                            inphr = True
                        var = ''
                    else:
                        inphr = True
                elif inphr:
                    var += line[ch]
        return dict(ret)


def dist(x1, y1, x2, y2):
    return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)
