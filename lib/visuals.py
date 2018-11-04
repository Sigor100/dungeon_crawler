import pygame
import generation
import os
import entities
import settings as s
from math import sqrt, sin, cos

directory = '/debug'

shadow_mode = 2  # set to 2 for the whole map to be visible from the start

# IMPORTANT: Don't delete comments in this file
selection_type = True  # false = box    true = circle
shadow_map = []
dirx = (0, 1, 0, -1)
diry = (-1, 0, 1, 0)
projectpath = os.getcwd()
os.path.exists(projectpath)
shadow_texture = pygame.image.load(projectpath + directory + '/resources/textures/void.png')
UI_textures = [['slot', 'slot_selected'],
               [['move_NW', 'move_N', 'move_NE'], ['move_W', 'move_stay', 'move_E'], ['move_SW', 'move_S', 'move_SE']],
               [['blank', 'backpack', 'blank'], ['sword', 'blank', 'shield'], ['potion', 'potion', 'potion']],
               'crosshair',
               # ['sword'],
               ['sword', 'shield', 'potion', 'potion', 'potion', 'backpack']]

view_range = 4

pygame.init()

# IMG IMPORT
backpack_background = pygame.image.load(projectpath + "/resources/backpack.png")

gameDisplay = pygame.display.set_mode((s.display_width, s.display_height))
pygame.display.set_caption("dungeon crawler")
gameDisplay.fill(s.background)


def drawscreen(x, y, selected):
    global shadow_map
    calculateshadows()
    for i in range(0, generation.curmap.height):
        for j in range(0, generation.curmap.width):
            texture = []
            if shadow_map[i][j] != 0:
                texture.append(generation.tilesprot[generation.curmap.tiles[i][j]].texture)
                if not generation.curmap.entities[i][j] == -1 and shadow_map[i][j] == 2:
                    texture.append(entities.entitiesprot[generation.curmap.entities[i][j].id].texture)
            else:
                texture.append(shadow_texture)
            for t in texture:
                if shadow_map[i][j] == 1:
                    blit_alpha(gameDisplay, t, [(j * s.box_size - x), i * s.box_size - y], 50)
                else:
                    gameDisplay.blit(t, [(j * s.box_size - x), i * s.box_size - y])

    if entities.player.state == 2:
        gameDisplay.blit(UI_textures[3], [(entities.player.x + entities.player.target[0]) * s.box_size - x,
                                          (entities.player.y + entities.player.target[1]) * s.box_size - y])
    draw_hud(selected)
    draw_enemie_hp(x, y)
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


def draw_hud(selected):  # todo
    pygame.draw.rect(gameDisplay, s.grey, (245, 95, 235, 30))  # x, y, height, width
    pygame.draw.rect(gameDisplay, s.red, (250, 100, 225, 20))  # x, y, height, width
    # pygame.draw.rect(gameDisplay, red, (250, 100, 2.25*player_hp, 20))  # x, y, height, width
    # pygame.draw.circle(gameDisplay, white, (100, 100), 100)  # x, y, radius
    if not selection_type:
        draw_selection(s.display_width - 3 * s.box_size, s.display_height - 3 * s.box_size)
    elif entities.player.state == 1 and selection_type is True:
        draw_selection_circle(selected)


def draw_selection(x, y):
    for i in range(0, 3):
        for j in range(0, 3):
            if entities.player.choice == [i + entities.player.minchoice[0], j + entities.player.minchoice[1]]:
                gameDisplay.blit(UI_textures[0][1], [x + i * s.box_size, y + j * s.box_size])
            else:
                gameDisplay.blit(UI_textures[0][0], [x + i * s.box_size, y + j * s.box_size])
            if entities.player.state == 0 or entities.player.state == 2:
                gameDisplay.blit(UI_textures[1][j][i], [x + i * s.box_size, y + j * s.box_size])
            elif entities.player.state == 1:
                gameDisplay.blit(UI_textures[2][j][i], [x + i * s.box_size, y + j * s.box_size])


def draw_selection_circle(selected):
    # circle_list = []
    r = 100
    pygame.draw.circle(gameDisplay, s.grey, [int(s.display_width / 2), int(s.display_height / 2)], r)
    for p in range(0, len(UI_textures[4])):
        angle = int((360 / len(UI_textures[4])) * p)
        if 0 <= angle <= 90:
            y = r * cos(angle)
            x = r * sin(angle)
        elif 90 < angle <= 180:
            y = r * sin(angle) * -1
            x = r * cos(angle)
        elif 180 < angle <= 270:
            y = r * cos(angle) * -1
            x = r * sin(angle) * -1
        elif 270 < angle <= 360:
            y = r * sin(angle)
            x = r * cos(angle) * -1
        finy = int((s.display_height / 2) - 16 - y)
        finx = int((s.display_width / 2) - 16 + x)
        if selected == p:
            gameDisplay.blit(UI_textures[0][1], [finx, finy])
            print(finx, finy, angle)
        gameDisplay.blit(UI_textures[4][p], [finx, finy])


def draw_enemie_hp(camx, camy):
    for p in entities.active:
        x = p.x * s.box_size - camx
        y = (p.y * s.box_size - camy) + s.box_size
        pygame.draw.rect(gameDisplay, s.black, (x - 2, y - 2, 44, 8))  # x, y, height, width
        pygame.draw.rect(gameDisplay, s.red, (x, y, 40, 4))  # x, y, height, width


# def draw_aim(x, y, direction, r):   # r = range
# for p in range(0, r):


"""def drawbackpack():
gameDisplay.fill(background)
    #gameDisplay.blit(img_list[1], 100, 100)

    pygame.display.update()"""  # todo this sometime


def loadresinlist(l):
    for i in range(0, len(l)):
        if isinstance(l[i], list):
            loadresinlist(l[i])
        else:
            l[i] = pygame.image.load(projectpath + '/resources/textures/UI/' + l[i] + '.png')


def exitmenu():
    return 1


def init():
    global shadow_map, UI_textures

    shadow_map = getmap(shadow_mode)
    loadresinlist(UI_textures)
