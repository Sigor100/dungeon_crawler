import pygame
import os

directory = '/debug'

pygame.init()


class ItemPrototype:
    def __init__(self):
        self.name = ""
        self.width = 0
        self.height = 0
        self.value = 0
        self.texture = 0


class Item:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = False


class PrimaryWeapon:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.mindmg = 0
        self.maxdmg = 0
        self.dmgtype = 0  # 0 = physical   1 = magical idk more
        self.range = 0
        self.rotation = False


class Armor:
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
        self.satiation = 0  # from 0 to 100


itemprot = []
itemnames = []


def loaditems(path):
    global itemprot, itemnames

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        ret = ItemPrototype()
        ret.name = file.split('.', 1)[0]
        with open(path + '/' + file) as f:
            file = f.read()

        i = 0
        var = ''
        for ch in file:
            if ch == ' ' or ch == '/':
                if i == 0:
                    ret.name = var
                elif i == 1:
                    ret.width = int(var)
                elif i == 2:
                    ret.height = int(var)
                elif i == 3:
                    ret.value = int(var)
                elif i == 4:
                    ret.texture = pygame.image.load(var)
                i += 1
                var = ''
            else:
                var += ch
        # ret.drops.append(int(var))
        itemprot.append(ret)
        itemnames.append(ret.name)


def init():
    projectpath = os.getcwd().split('\\', 1)[0]
    print(projectpath)
    loaditems(projectpath + directory + '/resources/items')
