import pygame
from generation import smartrand
import combat
import settings as s
from util import *
import itemstats as l
import os

projectpath = ''

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


class Usable:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = False

        self.effect = 0
        self.range = 0


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
    if itemprot[id].type == 1:
        return Weapon(id, x, y)
    # if itemprot[id].type == 0:
    #    return Item(id, x, y)
    if itemprot[id].type == 1:
        return Weapon(id, x, y)
    # elif itemprot[id].type == 2:
    #    return Usable(id, x, y)
    else:
        print('wtf')


def loaditems(path):
    global itemprot
    files = [path]
    for file in files:
        f = Parser(file)
        att = f.readall()

        ret = ItemPrototype()
        ret.name = att['name']
        ret.height = int(att['height'])
        ret.width = int(att['width'])
        ret.value = int(att['value'])
        ret.texture = pygame.image.load(s.directory + att['texture'])
        ret.type = l.types.index(att['type'])
        itemprot.append(ret)


def init():
    global projectpath

    loaditems(s.directory + '/items/excalibur.txt')

    for ret in itemprot:
        print(ret.name)
        print(ret.height)
        print(ret.width)
        print(ret.value)
        print(ret.texture)
        print(ret.type)
