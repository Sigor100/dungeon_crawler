import os
import visuals
import generation
import pygame
import random
from collisions import getpath

entitiesprot = []
entitynames = []
alive = []
player = 0
<<<<<<< HEAD

directory = '/debug'

=======
curmap = generation.curmap
>>>>>>> e1e3111fe367f330850df9a4aa65a2928aae8b10

class EntityPrototype:
    def __init__(self):
        self.name = ''
        self.minhp = 0
        self.maxhp = 0
        self.mindmg = 0
        self.maxdmg = 0
        self.minac = 0
        self.maxac = 0
        self.texture = 0
        self.drops = []


class Entity:
    def __init__(self, id, x, y):
        print(entitiesprot)
        print('entity', id, x, y)
        self.id = id
        # with entitiesprot[id] as e:
        #    with random.randint as r:
        #        self.hp = r(e.minhp, e.maxhp)
        #        self.dmg = r(e.mindmg, e.maxdmg)
        #        self.ac = r(e.minac, e.maxac)
        #    self.drops = e.drops
        self.moves = []
        self.x = x
        self.y = y
        generation.curmap.alive[y][x] = self.id
        alive.append(self)

    def goto(self, x, y):
        generation.curmap.alive[self.y][self.x] = -1
        self.moves = getpath([self.x, self.y], [x, y])
        generation.curmap.alive[self.y][self.x] = self.id

    def step(self):
        print(self.moves)
        if not len(self.moves) == 0:  # and not generation.curmap.alive[self.moves[1]][self.moves[0]] == 0:
            generation.curmap.alive[self.y][self.x] = -1
            self.x = self.moves[0][0]
            self.y = self.moves[0][1]
            generation.curmap.alive[self.y][self.x] = self.id
            del self.moves[0]


class Player(Entity):
    def __init__(self):
        global player
        self.id = 0
        self.moves = []
        self.hp = 15
        self.lvl = 1
        self.x = generation.curmap.startpos[0]
        self.y = generation.curmap.startpos[1]
        generation.curmap.alive[self.y][self.x] = self.id
        player = self

    def move(self, pos):
        if not generation.tilesprot[generation.curmap.tiles[self.y + pos[1]][self.x + pos[0]]].collision == 0 \
                and generation.curmap.alive[self.y + pos[1]][self.x + pos[0]] == -1:
            generation.curmap.alive[self.y][self.x] = -1
            self.x += pos[0]
            self.y += pos[1]
            generation.curmap.alive[self.y][self.x] = 0


def loadenemies(path):
    global entitiesprot

    ret = EntityPrototype()
    ret.texture = pygame.image.load(path[:-18] + directory + '/resources/textures/player.png')
    entitiesprot.append(ret)

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        ret = EntityPrototype()
        ret.name = file.split('.', 1)[0]
        with open(path + '/' + file) as f:
            file = f.read()

        i = 0
        ret.drops = []
        var = ''
        for ch in file:
            if ch == ' ':
                if i == 0:
                    ret.minhp = int(var)
                elif i == 1:
                    ret.maxhp = int(var)
                elif i == 2:
                    ret.mindmg = int(var)
                elif i == 3:
                    ret.maxdmg = int(var)
                elif i == 4:
                    ret.minac = int(var)
                elif i == 5:
                    ret.maxac = int(var)
                elif i == 6:
                    ret.texture = pygame.image.load(os.getcwd() + directory + '/' + var)
                else:
                    ret.drops.append(int(var))
                i += 1
                var = ''
            else:
                var += ch
        ret.drops.append(int(var))
        entitiesprot.append(ret)
        entitynames.append(ret.name)


def turn():
    for i in alive:
        generation.curmap.generategrid()
        if visuals.shadow_map[i.y][i.x] == 2:
            i.goto(player.x, player.y)
        i.step()


def init():
    projectpath = os.getcwd()  # .split('\\', 1)[0]
    loadenemies(projectpath + '/resources/enemies')


def random_spawn(id):
    spawnrange = 7
    while True:
        x = random.randint(0, generation.curmap.width)
        y = random.randint(0, generation.curmap.height)
        for a in alive:
            if visuals.check_distance(x, y, alive[a][2], alive[a][3]) > spawnrange and curmap.tiles[y][x] == 2:
                Entity(id, x, y)
                break
            else:
                if spawnrange == 0:
                    print("couldn't randomly spawn enemy")
                    break
                spawnrange -= 1

