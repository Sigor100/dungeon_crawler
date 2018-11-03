import pygame
import generation
import os
import collisions
import entities
import settings as s
from math import sqrt

shadow_mode = 0  # set to 2 for the whole map to be visible from the start

# IMPORTANT: Don't delete comments in this file
shadow_map = []
dirx = (0, 1, 0, -1)
diry = (-1, 0, 1, 0)
projectpath = os.getcwd()
os.path.exists(projectpath)
shadow_texture = pygame.image.load(projectpath + '/resources/textures/void.png')

view_range = 4

pygame.init()

# IMG IMPORT
backpack_background = pygame.image.load(projectpath + "/resources/backpack.png")

gameDisplay = pygame.display.set_mode((s.display_width, s.display_height))
pygame.display.set_caption("dungeon crawler")
gameDisplay.fill(s.background)


def drawscreen(x, y):
    global shadow_map
    calculateshadows()
    for i in range(0, generation.curmap.height):
        for j in range(0, generation.curmap.width):
            texture = []
            if shadow_map[i][j] != 0:
                texture.append(generation.tilesprot[generation.curmap.tiles[i][j]].texture)
                if not generation.curmap.entities[i][j] == -1 and shadow_map[i][j] == 2:
                    texture.append(entities.entitiesprot[generation.curmap.entities[i][j]].texture)
            else:
                texture.append(shadow_texture)
            for t in texture:
                if shadow_map[i][j] == 1:
                    # print("alpha")
                    blit_alpha(gameDisplay, t, [(j * s.box_size - x), i * s.box_size - y], 50)
                else:
                    gameDisplay.blit(t, [(j * s.box_size - x), i * s.box_size - y])

    draw_hud()
    pygame.display.update()
    gameDisplay.fill(s.background)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def calculateshadows():
    global shadow_map
    checked = getmap(0)
    x = entities.player.x
    y = entities.player.y
    for p in range(0, len(shadow_map), 1):
        for p1 in range(0, len(shadow_map[0]), 1):
            if shadow_map[p][p1] == 2:
                shadow_map[p][p1] = 1
    tocheck = []
    for i in range(0, len(dirx)):
        if check_distance(x, y, x + dirx[i], y + diry[i]) < view_range:
            tocheck.append([x + dirx[i], y + diry[i]])
        else:
            print(x, y, x + dirx[i], y + diry[i])
    for i in tocheck:
        if not checked[i[1]][i[0]] == 1:
            checked[i[1]][i[0]] = 1
            shadow_map[i[1]][i[0]] = 2
            if generation.tilesprot[generation.curmap.tiles[i[1]][i[0]]].name == 'floor':
                for j in range(0, len(dirx)):
                    if check_distance(x, y, i[0] + dirx[j], i[1] + diry[j]) < view_range:
                        tocheck.append([i[0] + dirx[j], i[1] + diry[j]])


def check_distance(x1, y1, x2, y2):
    a = int(abs(x1 - x2) ** 2)
    b = int(abs(y1 - y2) ** 2)
    c = int(sqrt(a + b))
    # print("distance: ", c)
    return c


def getmap(n):
    ret_map = []
    for p in range(0, generation.curmap.height):
        a = []
        for q in range(0, generation.curmap.width):
            a.append(n)
        ret_map.append(a)
    return ret_map


def draw_hud():  # todo
    pygame.draw.rect(gameDisplay, s.grey, (245, 95, 235, 30))  # x, y, height, width
    pygame.draw.rect(gameDisplay, s.red, (250, 100, 225, 20))  # x, y, height, width
    # pygame.draw.rect(gameDisplay, red, (250, 100, 2.25*player_hp, 20))  # x, y, height, width
    # pygame.draw.circle(gameDisplay, white, (100, 100), 100)  # x, y, radius


"""def drawbackpack():
gameDisplay.fill(background)
	#gameDisplay.blit(img_list[1], 100, 100)

	pygame.display.update()"""  # todo this sometime


def init():
    global shadow_map
    shadow_map = getmap(shadow_mode)
