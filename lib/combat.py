import generation as g
import entities as e
import util as u

damagemap = []


class Attack:
    def __init__(self, tiles, range):
        self.tiles = tiles
        self.range = range

    def use(self, x, y, force):
        global damagemap
        for i in self.tiles:
            damagemap[i[1] + y][i[0] + x] += i[2] * force


def applydamage():
    global damagemap
    for i in range(0, g.curmap.height):
        for j in range(0, g.curmap.width):
            if not g.curmap.entities[i][j] == -1:
                g.curmap.entities[i][j].hurt(damagemap[i][j])
    damagemap = u.getmap(0, g.curmap.height, g.curmap.width)


def init():
    global damagemap

    damagemap = u.getmap(0, g.curmap.height, g.curmap.width)
