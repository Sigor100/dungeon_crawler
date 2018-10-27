import os
import generation
import settings as s
import collisions
import random
import visuals


"""class Enemy:
    def __init__(self, id, lvl, type, name, damage, hp, drop_min, drop_max):
        self.id = id
        self.lvl = lvl
        self.type = type  # 0 = melee	1 = ranged  2 = both
        self.name = name
        self.damage = damage
        self.hp = hp
        self.drop_min = drop_min
        self.drop_max = drop_max"""


alive_enemies_list = []  # [id, active, hp, x, y]
active_enemies = []
enemies_map = []
curmap = generation.getmap()
max_lvl = 1
box_size = s.box_size
enemy_list = []
a = []
for p in range(0, len(curmap.tiles)):
    a = []
    for q in range(0, len(curmap.tiles[0])):
        a.append(0)
    enemies_map.append(a)
print("enemies map: ", len(enemies_map), len(enemies_map[0]))


def init():
    direct = os.getcwd()
    # direct = direct[:-4]

    global enemies_map
    global enemy_list
    file_list = []

    for p in range(1, 2):
        enemy_file = open(direct + "/resources/enemies/enemy" + str(p) + ".txt")
        enemy_file = list(enemy_file)
        enemy_file = str(enemy_file)
        enemy_file = list(enemy_file)
        file_list.append(enemy_file)

    for p in range(0, len(file_list), 1):
        file_list[p] = file_list[p][2:]
        file_list[p] = file_list[p][:-2]

    h_list = []
    h_list2 = []

    for p in range(0, len(file_list), 1):
        if file_list[p][0] == "0":
            for p1 in range(0, len(file_list[p])):
                if file_list[p][p1] != " ":
                    h_list.append(file_list[p][p1])
                else:
                    h_list2.append("".join(h_list))
                    h_list = []
            h_list2.append("".join(h_list))
            h_list = []
            enemy_list.append(h_list2)
            h_list2 = []
    print("enemy_list: ", enemy_list)
    for p in range(1, len(enemy_list)):
        print(enemy_list[p][1])
        #enemy_list[p] = Enemy(enemy_list[p][0], enemy_list[p][1], enemy_list[p][2], enemy_list[p][3],
                              #enemy_list[p][4], enemy_list[p][5], enemy_list[p][6], enemy_list[p][7])


def spawn_enemy(x=-1, y=-1, id=-1, lvl=-1):
    global enemies_map
    temp = []
    """if x == -1 and y == -1:
        x = random.randint(0, s.display_width)
        y = random.randint(0, s.display_height)"""
    if x == -1 and y == -1:
        #done = False
        print("losuje x i y")
        # while not done:    #todo: can do this better
        x = random.randint(0, curmap.width - 1)
        y = random.randint(0, curmap.height - 1)
    if [x, y] not in visuals.get_discoverymap() and curmap.tiles[y][x] == 2:
        # done = True
        print("x,y: ", x, y)
        if lvl == -1 and id != -1:
            enemies_map[y][x] = id
            alive_enemies_list.append([id, 0, enemy_list[id + 1][5], x, y])
        elif lvl == -1 and id == -1:
            lvl = random.randint(1, max_lvl)
            for p in range(0, len(enemy_list), 1):
                if enemy_list[p][1] == lvl:
                    temp.append(enemy_list[p][0])
            enemies_map[y][x] = temp[random.randint(0, len(temp))]
        elif lvl != -1 and id != -1:
            enemies_map[y][x] = id
            alive_enemies_list.append([id, 0, int(enemy_list[id-1][5]), x, y])
        elif lvl != -1 and id == -1:
            for p in range(0, len(enemy_list), 1):
                if enemy_list[p][1] == lvl:
                    temp.append(enemy_list[p][0])
            enemies_map[y][x] = temp[random.randint(0, len(temp))]


def give_active_enemies(temp_list):
    for p in range(0, len(temp_list),1):
        if temp_list[p] == [alive_enemies_list[p][3], alive_enemies_list[p][4]]:
            active_enemies.append(alive_enemies_list[p][0], alive_enemies_list[p][3], alive_enemies_list[p][4])


def enemy_turn(x, y):
    #if len(alive_enemies_list) > 0:
    for p in range(0, len(alive_enemies_list), 1):
        try:
            print(collisions.getpath([alive_enemies_list[p][3], alive_enemies_list[p][4]], [x, y]))
        except:
            print("ERROR: p: ", p, len(alive_enemies_list), alive_enemies_list)
        if alive_enemies_list[p][2] <= 0:
            enemies_map[alive_enemies_list[p][4]][alive_enemies_list[p][3]] = 0
            active_enemies.remove(alive_enemies_list[p])
            del alive_enemies_list[p]
        """"#print("p: ", q, len(alive_enemies_list), alive_enemies_list)
        if alive_enemies_list[p][2] <= 0:
            alive_enemies_list.remove(alive_enemies_list[p])           #HP
            #temp = 0"""
