import random


r = "nodebug"
debug = False
rooms = 10


curmap = 0
items = ["void", "wall", "floor", "door", "upstairs", "downstairs", "trap", "hero"]
roomtraits = ["entrance", "corridor", "regular", "traproom"]
roomlist = []
offx = 1
offy = 1


class Map:
    height = 0
    width = 0
    tiles = []
    startpos = [0, 0]
    endpos = [0, 0]
    rooms = []


class Room:
    xpos = 0
    ypos = 0
    height = 0
    width = 0
    doors = []
    trait = 0   # 0 - corridor, 1 - regular room, 2 - trap room
    tiles = []
    wtiles = 0


def collidable(n):
    #n = curmap.tiles[coords[0], coords[1]]
    if n == items.index("floor") or n == items.index("door")\
        or n == items.index("upstairs") or n == items.index("downstairs")\
            or n == items.index("trap") or n == 0:
        return True
    return False


def wallxy(width, height, n):
    coords = [0, 0]
    if n < width:
        coords[0] = n
    elif n < width + height - 1:
        coords[0] = width - 1
        coords[1] = n - width + 1
    elif n < 2 * width + height - 2:
        coords[0] = width - 1 - n + width + height - 2
        coords[1] = height - 1
    else:
        coords[0] = 0
        coords[1] = height - 1 - n + 2 * width + height - 3
    return coords


def doornumber(i, n):
    if i < 2 and (n == roomtraits.index("regular") or n == roomtraits.index("corridor")):
        return random.randint(0, 2)
    elif n == roomtraits.index("entrance"):
        return 3
    else:
        return 0


def smartrand(start, fin):
    if start >= fin:
        return start
    else:
        if r == "floor":
            return start
        elif r == "ceiling":
            return fin
        else:
            return random.randint(start, fin)


def inside(a, b):
    if a[0] > b[0] and a[0] < b[0] + b[2] - 1 and a[1] > b[1] and a[1] < b[1] + b[3] - 1:
        return True
    return False


def intersection(a, b):
    if inside([a[0], a[1]], b) or inside([a[0] + a[2], a[1]], b)\
            or inside([a[0], a[1] + a[3]], b) or inside([a[0] + a[2], a[1] + a[3]], b):
        return True
    return False


def addmaprow(dir):
    global curmap
    global offx, offy
    if dir[1] < 0:
        curmap.tiles.insert(0, [])
        for i in range(0, curmap.width):
            curmap.tiles[0].append(items.index("void"))
        curmap.height += 1
        offy += 1
    elif dir[1] > 0:
        curmap.tiles.append([])
        for i in range(0, curmap.width):
            curmap.tiles[curmap.height].append(items.index("void"))
        curmap.height += 1
    if dir[0] > 0:
        for i in range(0, curmap.height):
            curmap.tiles[i].append(items.index("void"))
        curmap.width += 1
    elif dir[0] < 0:
        for i in range(0, curmap.height):
            curmap.tiles[i].insert(0, items.index("void"))
        curmap.width += 1
        offx += 1

def genroom(y, x, height, width, trait):
    # set variables
    cls = Room()
    cls.height = height
    cls.width = width
    cls.tiles = []
    cls.xpos = x
    cls.ypos = y
    cls.wtiles = (2 * (cls.height + cls.width) - 4)

    # generate room
    for i in range(0, cls.height):
        templist = []
        for j in range(0, cls.wtiles):
            if j == 0 or j == cls.width - 1 or i == 0 or i == cls.height - 1:
                templist.append(items.index("wall"))
            else:
                if trait == roomtraits.index("traproom"):
                    templist.append(items.index("door"))
                else:
                    templist.append(items.index("floor"))
        cls.tiles.append(templist)

    if trait == roomtraits.index("entrance"):
        cls.tiles[int(height/2)][int(width/2)] = items.index("upstairs")
    print(y + offy + cls.ypos, x + offx + cls.xpos)
    for y in range(0, cls.height):
        for x in range(0, cls.width):
            curmap.tiles[y + offy + cls.ypos][x + offx + cls.xpos] = cls.tiles[y][x]
    roomlist.append(cls)
    curmap.rooms.append([x + offx, y + offy, width, height])


def generatevalidroom():
    pos = 0
    direc = 0
    while True:
        while True:
            room_no = smartrand(0, len(roomlist) - 1)
            troom = roomlist[room_no]
            pos = wallxy(troom.width, troom.height, random.randint(0, 2 * troom.width + 2 * troom.height - 4))
            if troom.tiles[pos[1]][pos[0]] == items.index("wall") and\
                    (troom.trait == roomtraits.index("corridor") or troom.trait == roomtraits.index("regular") or
                     troom.trait == roomtraits.index("entrance")):
                pos[0] += troom.xpos
                pos[1] += troom.ypos
                break
        a = []
        print("map: ", curmap.height, curmap.width)
        print(pos[1] + offy, pos[0] + offx)
        print(pos[1] + offy - 1, pos[0] + offx)
        a.append(curmap.tiles[pos[1] + offy - 1][pos[0] + offx])
        print(pos[1] + offy, pos[0] + offx + 1)
        a.append(curmap.tiles[pos[1] + offy][pos[0] + offx + 1])
        print(pos[1] + offy + 1, pos[0] + offx)
        a.append(curmap.tiles[pos[1] + offy + 1][pos[0] + offx])
        print(pos[1] + offy, pos[0] + offx - 2)
        a.append(curmap.tiles[pos[1] + offy][pos[0] + offx - 1])
        twalls = 0
        tfloors = 0
        tvoids = 0
        for i in range(0, 4):
            if a[i] == items.index("wall"):
                twalls += 1
            if a[i] == items.index("floor"):
                tfloors += 1
            if a[i] == items.index("void"):
                tvoids += 1
                direc = i
        print(pos)
        print(direc)
        if twalls == 2 and tfloors == 1 and tvoids == 1:
            break
    # set target tile
    print("following is imortaint")
    rwidth = (random.choice([2, 6])) * 2 + 1
    rheight = (random.choice([2, 6])) * 2 + 1
    rpos = [0, 0]
    if direc == 0:
        rpos = [pos[0] - smartrand(1, rwidth - 2), pos[1] - rheight + 1]
    elif direc == 1:
        rpos = [pos[0], pos[1] - smartrand(1, rheight - 2)]
    elif direc == 2:
        rpos = [pos[0] - smartrand(1, rwidth - 2), pos[1]]
    elif direc == 3:
        rpos = [pos[0] + 1 - rwidth, pos[1] - smartrand(1, rheight - 2)]
    print(rpos)
    print(rwidth)
    print(rheight)
    # stretch the map if necessary
    while rpos[0] + offx < 1:
        addmaprow([-1, 0])
    while rpos[1] + offy < 1:
        addmaprow([0, -1])
    while rpos[0] + offx + rwidth > curmap.width - 1:
        addmaprow([1, 0])
    while rpos[1] + offy + rheight > curmap.height - 1:
        addmaprow([0, 1])

    # generate!
    genroom(rpos[1], rpos[0], rheight, rwidth, roomtraits.index("regular"))
    curmap.tiles[pos[1] + offy][pos[0] + offx] = items.index("door")
    return 0


def getmap(update=False):
    global curmap
    global roomlist
    global offx, offy
    if curmap == 0 or update:
        curmap = Map()
        curmap.width = random.choice([3, 5]) * 2 + 1
        curmap.height = random.choice([3, 5]) * 2 + 1
        curmap.rooms = []
        offx = 1
        offy = 1
        curmap.startpos = [int((curmap.width - 1) / 2) - offx, int((curmap.height - 1) / 2) - offy]

        # set map to all 0s
        curmap.tiles = []
        for y in range(0, curmap.height):
            temp = []
            for x in range(0, curmap.width):
                temp.append(items.index("void"))
            curmap.tiles.append(temp)

        # generate rooms
        roomlist = []
        genroom(0, 0, curmap.height - 2, curmap.width - 2, roomtraits.index("entrance"))
        for i in range(0, rooms - 1):
            generatevalidroom()

        # apply final changes
        curmap.startpos[0] = curmap.startpos[0] + offx
        curmap.startpos[1] = curmap.startpos[1] + offy

        if debug:
            for i in range(0, curmap.height):
                print(curmap.tiles[i])
            for i in range(0, len(curmap.rooms)):
                print(curmap.rooms[i])

    return curmap
