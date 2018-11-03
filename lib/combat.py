import generation as g

damagemap = []


class Attack:
    tiles = []

    def use(self, force):
        global damagemap

        for i in self.tiles:
            damagemap[i[1]][i[0]] += i[2] * force


def setmap(usemap):
    usemap = []
    for i in range(0, g.curmap.height):
        temp = []
        for j in range(0, g.curmap.width):
            temp.append(0.0)
        usemap.append(temp)


def init():
    global damagemap


    print(damagemap)
