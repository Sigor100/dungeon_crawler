import os
import visuals
import generation
import pygame
import random
import settings as s
from collisions import getpath
import equipment

entitiesprot = []
entitynames = []
alive = []
active = []
player = 0


directory = '/debug'

curmap = generation.curmap


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
        self.x = x
        self.y = y
        # with entitiesprot[id] as e:
        #    with random.randint as r:
        self.hp = random.randint(entitiesprot[id].minhp, entitiesprot[id].maxhp)
        self.dmg = random.randint(entitiesprot[id].mindmg, entitiesprot[id].maxdmg)
        #self.ac = r(e.minac, e.maxac)
        #    self.drops = e.drops
        self.moves = []

        generation.curmap.entities[y][x] = self
        alive.append(self)

    def goto(self, x, y):
        generation.curmap.entities[self.y][self.x] = -1
        self.moves = getpath([self.x, self.y], [x, y])
        generation.curmap.entities[self.y][self.x] = self

    def step(self):
        print(self.moves)
        if not len(self.moves) == 0:  # and not generation.curmap.alive[self.moves[1]][self.moves[0]] == 0:
            generation.curmap.entities[self.y][self.x] = -1
            self.x = self.moves[0][0]
            self.y = self.moves[0][1]
            generation.curmap.entities[self.y][self.x] = self
            del self.moves[0]

    def hurt(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            generation.curmap.entities[self.y][self.x] = 0
            alive.remove(self)


class Player(Entity):
    def __init__(self):
        global player
        self.id = 0
        self.moves = []
        self.hp = 25
        self.lvl = 1
        self.charm = []
        self.hunger = 100  # from 0 to 100
        self.Armor = [0, 0, 0]
        self.Usable = [equipment.makeitem(1, 0, 0), 2, 3, 4, 5] # main weapon, off-hand weapon, slots 1 - 3
        self.charm = 0
        self.hunger = 100  # from 0 to 100
        self.x = generation.curmap.startpos[0]
        self.y = generation.curmap.startpos[1]

        self.state = 0  # 0 - walking, 1 - choosing weapon, 2 - aiming
        self.choice = [0, 0]
        self.maxchoice = [1, 1]
        self.minchoice = [-1, -1]
        self.choices = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.using = 0
        self.pressed = False
        self.target = [self.x, self.y]

        generation.curmap.entities[self.y][self.x] = self
        player = self

    def move(self, pos):
        if not generation.tilesprot[generation.curmap.tiles[self.y + pos[1]][self.x + pos[0]]].collision == 0 \
                and generation.curmap.entities[self.y + pos[1]][self.x + pos[0]] == -1:
            generation.curmap.entities[self.y][self.x] = -1
            self.x += pos[0]
            self.y += pos[1]
            generation.curmap.entities[self.y][self.x] = self

    def resolve(self, direction):
        if direction == [0, 0]:
            self.pressed = False
            if self.state == 0:
                self.choice = [0, 0]
        else:
            if self.state == 0:
                self.choice = direction
                self.move(direction)
            # elif self.state == 1:
            #    self.choice = [direction[0] - self.minchoice[0], direction[1] - self.minchoice[1]]
            elif self.state == 1:
                if not self.pressed:
                    self.choice[0] += direction[0]
                    self.choice[1] += direction[1]
                    if self.choice[0] > self.maxchoice[0]:
                        self.choice[0] = self.maxchoice[0]
                    elif self.choice[0] < self.minchoice[0]:
                        self.choice[0] = self.minchoice[0]
                    if self.choice[1] > self.maxchoice[1]:
                        self.choice[1] = self.maxchoice[1]
                    elif self.choice[1] < self.minchoice[1]:
                        self.choice[1] = self.minchoice[1]
                    self.pressed = True
            elif self.state == 2:
                self.choice = direction
                self.move(direction)
                self.choice[0] += direction[0]
                self.choice[1] += direction[1]

    def changestate(self, n):
        if n == 0:
            self.state = 0
            self.choice = [0, 0]
            self.maxchoice = [1, 1]
            self.minchoice = [-1, -1]
            self.choices = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.using = 0
        elif n == 1:
            self.choices = [0, 0, 0, self.Usable[0], 0, self.Usable[1], self.Usable[2], self.Usable[3], self.Usable[4]]
            self.choice = [0, 0]
            self.state = 1
        if n == 2:
            self.choices = equipment.itemprot[self.using.id].choices
            self.choice = [0, 0]
            self.target = [0, 0]
            self.state = 2
        print(self.state)

    def action(self, n):
        if n == 1:
            if self.state == 0:
                self.changestate(1)
            elif self.state == 1:
                print(self.choice)
                self.using = self.choices[s.directions.index(self.choice)]
                if not self.using == 0:
                    self.changestate(2)
                    print(self.using)
            elif self.state == 2:
                a = self.using.choose(self.choice)
                if not a == 0:
                    self.using.attacks[a].use(self.target[0], self.target[1], self.calculateforce())
                    self.changestate(0)
        if n == 2:
            if self.state == 0:
                visuals.exitmenu()
            elif self.state == 1:
                self.changestate(0)
            elif self.state == 2:
                self.changestate(1)

    def calculateforce(self):
        return 1


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
    global active
    for i in alive:
        generation.curmap.generategrid()
        if visuals.shadow_map[i.y][i.x] == 2:
            active.append(i)
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
                if spawnrange == 5:
                    print("couldn't randomly spawn enemy")
                    break
                spawnrange -= 1


