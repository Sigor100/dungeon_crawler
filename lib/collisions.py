import generation

disablecollisions = False  # set to true for debug
pathfindingdebug = False

curmap = generation.getmap()
dirx = [0, 1, 1, 1, 0, -1, -1, -1]
diry = [-1, -1, 0, 1, 1, 1, 0, -1]
iii = 0

box_size = 32
hero_id = 5
acc_block = 4


def collisions(x, y, d):
    if generation.collidable(whatobject(x + d[1], y + d[0])) or disablecollisions:
        return True
    else:
        return False


def putonmap(x, y):
    global acc_block
    acc_block = curmap.tiles[int(y / box_size)][int(x / box_size)]
    curmap.tiles[int(y / box_size)][int(x / box_size)] = hero_id


def takeoffmap(x, y):
    curmap.tiles[int(y / box_size)][int(x / box_size)] = acc_block


def get_acc_block():
    return acc_block


def whatobject(x, y):
    x = int(x / 32)
    y = int(y / 32)
    return curmap.tiles[y][x]


def inroom(pos, i):
    if pos[0] > curmap.rooms[i][0]\
        and pos[0] < (curmap.rooms[i][0] + curmap.rooms[i][2] - 1)\
        and pos[1] > curmap.rooms[i][1]\
        and pos[1] < (curmap.rooms[i][1] + curmap.rooms[i][3] - 1):
        return True
    return False


def onroom(pos, i):

    if (pos[0] == curmap.rooms[i][0]
            or pos[0] == curmap.rooms[i][0] + curmap.rooms[i][2] - 1)\
        and (pos[1] == curmap.rooms[i][1]
            or pos[1] == curmap.rooms[i][1] + curmap.rooms[i][3] - 1):
        return True
    return False

def findpath(spos, epos):
    return -1


def getpath(spos, epos):
    sroom = -1
    eroom = -1
    for i in range(0, len(curmap.rooms)):
        if generation.onroom(spos, i):
            sroom = i
            break
    if sroom == -1:
        for i in range(0, len(curmap.rooms)):
            if generation.inroom(spos, i):
                sroom = i
                break
    for i in range(0, len(curmap.rooms)):
        if generation.onroom(spos, i):
            eroom = i
            break
    if eroom == -1:
        for i in range(0, len(curmap.rooms)):
            if generation.inroom(spos, i):
                eroom = i
                break
    if sroom == eroom:
        return findpath(spos, epos)
    return -1


def legacyfindpath(spos, epos, gcolmap):
    global iii
    colmap = []
    gcolmap[spos[1]][spos[0]] = 1
    for i in range(0, curmap.height):
        a = []
        for j in range(0, curmap.width):
            a.append(gcolmap[i][j])
        colmap.append(a)

    if pathfindingdebug:
        print('wow ' + str(iii))
        print(spos)
    iii += 1
    realret = []
    for i in range(0, len(dirx)):
        if [spos[0] + dirx[i], spos[1] + diry[i]] == epos:
            return [i]
        elif colmap[spos[1] + diry[i]][spos[0] + dirx[i]] == 0 and generation.collidable(curmap.tiles[spos[1] + diry[i]][spos[0] + dirx[i]]):
            ret = legacyfindpath([spos[0] + dirx[i], spos[1] + diry[i]], epos, colmap)
            if ret != -1:
                ret.insert(0, i)
                if len(ret) < len(realret) or len(realret) == 0:
                    realret = ret
    if len(realret) == 0:
        return -1
    return realret


def legacygetpath(spos, epos):
    iii = 0
    colmap = []
    for i in range(0, curmap.height):
        a = []
        for j in range(0, curmap.width):
            a.append(0)
        colmap.append(a)

    if spos[0] < 0 or spos[1] < 0 or epos[0] < 0 or epos[1] < 0 or \
            spos[0] >= curmap.width or spos[1] >= curmap.height or \
            epos[0] >= curmap.width or epos[1] >= curmap.height:
        print("out of range")
        return 0
    if not generation.collidable(curmap.tiles[spos[1]][spos[0]]) \
            or not generation.collidable(curmap.tiles[spos[1]][spos[0]]):
        print("collision error")
        return 0
    print(legacyfindpath(spos, epos, colmap))
    return legacyfindpath(spos, epos, colmap)