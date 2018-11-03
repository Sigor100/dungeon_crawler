import generation as g

damagemap = []


class Attack:
    def __init__(self, pos):
        self.tiles = pos

    def use(self, x, y, force):
        global damagemap

        for i in self.tiles:
            damagemap[i[1] + y][i[0] + x] += i[2] * force


def setmap(usemap, n=0):
    usemap = []
    for i in range(0, g.curmap.height):
        temp = []
        for j in range(0, g.curmap.width):
            temp.append(n)
        usemap.append(temp)


def applydamage():
    for i in range(0, g.curmap.height):
        for j in range(0, g.curmap.width):
            if not g.curmap.entities[i][j] == -1:
                g.curmap.entities[i][j].hurt(damagemap[i][j])
    setmap(damagemap, 0)


def init():
    global damagemap

    setmap(damagemap, 0)
    print(damagemap)
