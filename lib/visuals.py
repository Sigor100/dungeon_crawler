import pygame
import generation
import os
import collisions
from math import sqrt
import enemies
import settings as s

shadow_mode = 1  # set to 0 for the whole map to be visible from the start

# IMPORTANT: Don't delete comments in this file

direct = os.getcwd()
# direct = direct[:-4]
os.path.exists(direct)
# background = (25, 25, 25)
background = (0, 0, 0)
white = (255, 255, 255)
display_width = s.display_width
display_height = s.display_height
box_size = s.box_size
hero_x = 0
hero_y = 0
acc_block = collisions.acc_block
hero_id = 5
visible_thru = [2, 4]
visible_thru2 = [2, 4]
not_visible_thru = [1, 3, 4]
door_index = 3
visibility_list = []
discovered_map = []  # todo: discovered_map is now list, need to be map
# shadow_map = []

view_range = 4
view_mode = 2  # 0 or 1

pygame.init()

img_list = []
for num in range(0, 8):
    path = direct + "/resources/textures/img" + str(num) + ".png"
    img_list.append(pygame.image.load(path))
backpack_background = pygame.image.load(direct + "/resources/backpack.png")

curmap = generation.getmap()
"""shadow_map = []
for p in range(0, map.height):
    a = []
    for q in range(0, map.width):
        a.append(shadow_mode)
    shadow_map.append(a)"""

"""map = []
b = []
for p in range(0, 15):
	for p1 in range(0, 20):
		b.append(2)
	map.append(b)
	b = []
for p in range(0, 20):
	map[0][p] = 1
for p in range(0, 20):
	map[14][p] = 1"""

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("visuals test")
gameDisplay.fill(background)


def drawscreen(x, y):
    global discovered_map
    shadow_map = shadowupdate()
    # print("shadow map in drawscreen", shadow_map)
    for p in range(0, len(curmap.tiles), 1):
        for p1 in range(0, len(curmap.tiles[0]), 1):
            if shadow_map[p][p1] == 0:
                gameDisplay.blit(img_list[curmap.tiles[p][p1]], (-x + (box_size * p1), -y + (box_size * p)))
                # if enemies.enemies_map[p1][p] != 0:
                # gameDisplay.blit(8, (-x + (box_size * p1), -y + (box_size * p)))   # todo: still working on it
            else:
                # print([int(x/box_size), int(y/box_size)])
                if [p1, p] in discovered_map:
                    # print("yes")
                    blit_alpha(gameDisplay, img_list[curmap.tiles[p][p1]],
                               [(-x + (box_size * p1)), (-y + (box_size * p))], 50)
                else:
                    gameDisplay.blit(img_list[6], (-x + (box_size * p1), -y + (box_size * p)))
    pygame.display.update()
    gameDisplay.fill(background)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def get_discoverymap():
    return discovered_map


def get_box_size():
    return box_size


def check_distance(x1, y1, x2, y2):
    a = int(abs(x1 - x2) ** 2)
    b = int(abs(y1 - y2) ** 2)
    c = int(sqrt(a + b))
    # print("distance: ", c)
    return c


def refill_shadow_map():
    shadow_map = []
    global shadow_mode
    for p in range(0, curmap.height):
        a = []
        for q in range(0, curmap.width):
            a.append(shadow_mode)
        shadow_map.append(a)
    return shadow_map


def countplayervisibility(x, y):
    # if n == 0:
    # print("error: funcja z parametrem 0")
    x = int(x / box_size)
    y = int(y / box_size)
    # global shadow_map
    global visible_thru
    global visible_thru2
    global not_visible_thru
    global acc_block
    global view_range
    global visibility_list
    global discovered_map
    visibility_list = [[x, y]]
    acc_block = collisions.acc_block
    list2 = []
    # #print(collisions.get_acc_block())
    # #print(map.tiles[y][x])
    if 0 == 0:  # todo: don't remove this if
        end = False
        c = 1
        while not end:
            if curmap.tiles[y][x + c] in visible_thru:
                visibility_list.append([x + c, y])
                end1 = False
                end2 = False
                c1 = 1
                c2 = 1
                while not end1:
                    if curmap.tiles[y + c1][x + c] in visible_thru2:
                        visibility_list.append([x + c, y + c1])
                    elif curmap.tiles[y + c1][x + c] in not_visible_thru:
                        visibility_list.append([x + c, y + c1])
                        end1 = True
                    else:
                        end1 = True
                    c1 = c1 + 1
                while not end2:
                    if curmap.tiles[y - c2][x + c] in visible_thru2:
                        visibility_list.append([x + c, y - c2])
                    elif curmap.tiles[y - c2][x + c] in not_visible_thru:
                        visibility_list.append([x + c, y - c2])
                        end2 = True
                    else:
                        end2 = True
                    c2 = c2 + 1
            elif curmap.tiles[y][x + c] in not_visible_thru:
                visibility_list.append([x + c, y])
                end = True
            else:
                visibility_list.append([x + c, y])
                end = True
            c = c + 1
        end = False
        c = 1
        while not end:
            if curmap.tiles[y][x - c] in visible_thru:
                visibility_list.append([x - c, y])
                end1 = False
                end2 = False
                c1 = 1
                c2 = 1
                while not end1:
                    if curmap.tiles[y + c1][x - c] in visible_thru2:
                        visibility_list.append([x - c, y + c1])
                    elif curmap.tiles[y + c1][x - c] in not_visible_thru:
                        visibility_list.append([x - c, y + c1])
                        end1 = True
                    else:
                        end1 = True
                    c1 = c1 + 1
                while not end2:
                    if curmap.tiles[y - c2][x - c] in visible_thru2:
                        visibility_list.append([x - c, y - c2])
                    elif curmap.tiles[y - c2][x - c] in not_visible_thru:
                        visibility_list.append([x - c, y - c2])
                        end2 = True
                    else:
                        end2 = True
                    c2 = c2 + 1
            elif curmap.tiles[y][x - c] in not_visible_thru:
                visibility_list.append([x - c, y])
                end = True
            else:
                # visibility_list.append([x - c, y])
                end = True
            c = c + 1
        end = False
        c = 1
        while not end:
            if curmap.tiles[y - c][x] in visible_thru:
                visibility_list.append([x, y - c])
                end1 = False
                end2 = False
                c1 = 1
                c2 = 1
                while not end1:
                    if curmap.tiles[y - c][x + c1] in visible_thru2:
                        visibility_list.append([x + c1, y - c])
                    elif curmap.tiles[y - c][x + c1] in not_visible_thru:
                        visibility_list.append([x + c1, y - c])
                        end1 = True
                    else:
                        end1 = True
                    c1 = c1 + 1
                while not end2:
                    if curmap.tiles[y - c][x - c2] in visible_thru2:
                        visibility_list.append([x - c2, y - c])
                    elif curmap.tiles[y - c][x - c2] in not_visible_thru:
                        visibility_list.append([x - c2, y - c])
                        end2 = True
                    else:
                        end2 = True
                    c2 = c2 + 1
            elif curmap.tiles[y - c][x] in not_visible_thru:
                visibility_list.append([x, y - c])
                end = True
            else:

                end = True
            c = c + 1
        end = False
        c = 1
        while not end:
            if curmap.tiles[y + c][x] in visible_thru:
                visibility_list.append([x, y + c])
                end1 = False
                end2 = False
                c1 = 1
                c2 = 1
                while not end1:
                    if curmap.tiles[y + c][x + c1] in visible_thru2:
                        visibility_list.append([x + c1, y + c])
                    elif curmap.tiles[y + c][x + c1] in not_visible_thru:
                        visibility_list.append([x + c1, y + c])
                        end1 = True
                    else:
                        end1 = True
                    c1 = c1 + 1
                while not end2:
                    if curmap.tiles[y + c][x - c2] in visible_thru2:
                        visibility_list.append([x - c2, y + c])
                    elif curmap.tiles[y + c][x - c2] in not_visible_thru:
                        visibility_list.append([x - c2, y + c])
                        end2 = True
                    else:
                        end2 = True
                    c2 = c2 + 1
            elif curmap.tiles[y + c][x] in not_visible_thru:
                visibility_list.append([x, y + c])
                end = True
            else:
                end = True
            c = c + 1
        """elif collisions.acc_block == door_index:
        #print("door")
        qlist = []
        end = False
        c = 1
        #qlist = [[y, x + c], [y, x - c], [y + c, x], [y - c, x]]
        qlist = []
        for p in range(0, 4, 1):
            #print("p: ", p)
            if p == 0:
                qlist = []
                qlist.append(y)
                qlist.append(int(x + c))
            elif p == 1:
                qlist = [y, int(x - c)]
            elif p == 1:
                qlist = [int(y + c), x]
            elif p == 1:
                qlist = [int(y - c), x]
            while not end:
                if map.tiles[qlist[0], qlist[1]] in visible_thru:
                    visibility_list.append([qlist[1], qlist[0]])
                elif map.tiles[qlist[0], qlist[1]] in not_visible_thru:
                    visibility_list.append([qlist[1], qlist[0]])
                    end = True
                c = c + 1
                #qlist = [[y, x + c], [y, x - c], [y + c, x], [y - c, x]]"""
        # else:
        # #print("error: not acceptable acc_block: ", acc_block)
        # if n == 0:
        # print("n == 0, visibility list: ", visibility_list)
        """elif acc_block == door_index and n == 1:
        #print("door")
        a = []
        if view_mode == 0:
            for p in range(0, len(curmap.tiles)):
                for p1 in range(0, len(curmap.tiles[0])):
                    if check_distance(x, y, p1, p) < view_range:
                        visibility_list.append([p1, p])
        elif view_mode == 2:
            if n == 1:
                if len(visibility_list) > 0:
                    #print("0 w visilisity list  #1")
                if curmap.tiles[y][x + 1] in visible_thru:
                    countplayervisibility(x * box_size + box_size, y, 0)
                    countplayervisibility(x * box_size - box_size, y, 0)
                else:
                    countplayervisibility(x, y * box_size - box_size, 0)
                    countplayervisibility(x, y * box_size + box_size, 0)
                if len(visibility_list) > 0:
                    #print("0 w visilisity list  #2")
                #print("len visib",len(visibility_list))
                for p in range(0, len(visibility_list), 1):  # todo finish this
                    if check_distance(x, y, visibility_list[p][0], visibility_list[p][1]) < view_range:
                        #print("append w if")
                        a.append(visibility_list[p])
                visibility_list = []
                visibility_list = a
                #print("a: ", a)
                a = []
                #print("visibility list po funkcji: ", visibility_list)"""
    # else:
    # print("error: unknown index", acc_block)
    for p in range(0, len(visibility_list), 1):
        if visibility_list[p] not in discovered_map:
            discovered_map.append(visibility_list[p])
        if check_distance(x, y, visibility_list[p][0], visibility_list[p][1]) < view_range:
            list2.append(visibility_list[p])
    visibility_list = []
    visibility_list = list2

    """shadow_map = refill_shadow_map()
    for p in range(0, len(visibility_list)):
        try:
            shadow_map[visibility_list[p][1]][visibility_list[p][0]] = 0
        except:
            #print("error: shadow_map index out of range: ", visibility_list[p][0], visibility_list[p][1])"""


def shadowupdate():
    global visibility_list
    # print("visibility list in shadowUpDate: ", visibility_list)
    shadow_map = refill_shadow_map()
    for p in range(0, len(visibility_list)):
        try:
            shadow_map[visibility_list[p][1]][visibility_list[p][0]] = 0
        except IndexError:
            print("error: shadow_map index out of range: ", visibility_list[p][0], visibility_list[p][1])
    # #print(shadow_map)
    # for p in range(0,len(shadow_map)):
    # if 0 in shadow_map[p]:
    # print("0 w visilisity list  #4")
    visibility_list = []
    return shadow_map


# #print("shadowmap", shadow_map)


"""#print(int(y/box_size), int(x/box_size))
shadow_map[int(y/box_size)+1][int(x/box_size)] = 0
	shadow_map[int(y / box_size)][int(x / box_size)] = 0
	shadow_map[int(y / box_size)-1][int(x / box_size)] = 0
	shadow_map[int(y / box_size)][int(x / box_size)+1] = 0
	shadow_map[int(y / box_size)][int(x / box_size)-1] = 0
	shadow_map[int(y / box_size)-1][int(x / box_size)+1] = 0
	shadow_map[int(y / box_size)-1][int(x / box_size)-1] = 0
	shadow_map[int(y / box_size)+1][int(x / box_size)+1] = 0
	shadow_map[int(y / box_size)+1][int(x / box_size)-1] = 0"""

# #print(shadow_map)

"""def drawbackpack():
gameDisplay.fill(background)
	#gameDisplay.blit(img_list[1], 100, 100)

	pygame.display.update()"""  # todo fix this sometime
