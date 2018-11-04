import pygame
from generation import smartrand
import combat
import entities as e
import settings as s
import util as u
import itemstats as l
import os

projectpath = ''
directory = ''

pygame.init()


class ItemPrototype:
    def __init__(self):
        self.name = ""
        self.width = 0
        self.height = 0
        self.value = 0
        self.texture = 0
        self.type = 0
        self.data = []

    def use(self):
        if e.player.state != 4:
            e.player.changestate(4)
        else:
            e.player.changestate(0)


class Item:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = False


class Weapon:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = False

        '''self.mindmg = smartrand(int(itemprot[id].data[0]), int(itemprot[id].data[1]))
        self.maxdmg = smartrand(int(itemprot[id].data[2]), int(itemprot[id].data[3]))
        self.range = float(itemprot[id].data[4])
        self.attack = combat.Attack([[0, 0, 100]], 10)'''


class Potion:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = False

        self.effect = 0
        self.range = 0


class Backpack:
    def __init__(self):
        self.texture = pygame.image.load(s.directory + '/textures/UI/backpack.png')
        self.items = []
        self.space = u.getmap(0, 7, 10)
        self.id = 0

    def use(self):
        if e.player.state != 4:
            e.player.changestate(4)
        else:
            e.player.changestate(0)


'''class Armor:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.block = []  # [minblock, maxblock]   from 0 to 100


class Food:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.satiation = 0'''  # from 0 to 100

itemprot = []
itemnames = []


def makeitem(id, x, y):
    if itemprot[id].type == 0:
        return Item(id, x, y)
    if itemprot[id].type == 1:
        return Weapon(id, x, y)
    elif itemprot[id].type == 2:
        return Weapon(id, x, y)
    elif itemprot[id].type == 3:
        return Potion(id, x, y)
    else:
        print('wtf')
        return 0


def loaditems(path):
    global itemprot
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        f = u.Parser(path + '/' + file)
        att = f.readall()

        ret = ItemPrototype()
        ret.name = att['name']
        ret.height = int(att['height'])
        ret.width = int(att['width'])
        ret.value = int(att['value'])
        ret.texture = pygame.image.load(s.directory + att['texture'])
        ret.type = l.types.index(att['type'])
        itemprot.append(ret)
        itemnames.append(ret.name)


def init():
    itemprot.append(Backpack())
    itemnames.append('backpack')
    loaditems(s.directory + '/items')


def add_to_bp(item):
    obj = itemprot[id]
    for i in range(0, obj.height):
        for j in range(0, obj.width):
            itemprot[0].space[i + item.y][j + item.x] = 1
    itemprot[0].items.add(item)


'''def refresh_backpack():
    global backpack
    backpack = []
    temp = []
    for p in range(0, s.backpack_max_y):
        for p1 in range(0, s.backpack_max_x):
            temp.append(0)
        backpack.append(temp)
        temp = []
    for p in range(0, s.backpack_max_y):
        if type(object) in backpack[p]:
            for p1 in range(0, s.backpack_max_x):
                if type(object) in backpack[p][p1]:'''
