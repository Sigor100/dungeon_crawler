import random

curmap = 0
items = ["void", "wall", "floor", "door", "upstairs", "downstairs", "trap", "hero"]
roomtraits = ["entrance", "corridor", "regular", "traproom"]
roomlist = []


class Map:
    height = 0
    width = 0
    roomno = 0
    tiles = []
    startpos = [0, 0]
    endpos = [0, 0]


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
    if i < 2:
        return 2
    else:
        return 0



def genroom(y, x, height, width, parents, trait):
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
                    templist.append(items.index("trap"))
                else:
                    templist.append(items.index("floor"))
        cls.tiles.append(templist)
    print(cls.tiles)
    # generate doors
    doorret = []
    if trait == 0 or trait == 1:
        doors = doornumber(parents, trait)
        for i in range(0, doors):
            while True:
                ch = random.choice(range(0, 2 * (cls.height + cls.width) - 4))

                if ch == 0 or ch == cls.width - 1\
                        or ch == cls.width + cls.height - 2 or ch == cls.width * 2 + cls.height - 3:
                    continue

                co = wallxy(cls.width, cls.height, ch)
                cls.tiles[co[1]][co[0]] = items.index("door")
                dco = co[0], co[1]
                doorret.append(dco)
                break

    # traits
    if trait == roomtraits.index("entrance"):
        cls.tiles[int(height/2)][int(width/2)] = items.index("upstairs")
    roomlist.append(cls)
    return doorret


def getmap():
    global curmap
    if curmap == 0:

        doors = genroom(0, 0, random.choice([2, 4]) * 2 + 1, random.choice([2, 4]) * 2 + 1, 0, roomtraits.index("entrance"))
        while len(doors) > 0:
            #i
            break
            #genroom(random.choice([0, 6]) * 2 + 1, random.choice([0, 6]) * 2 + 1, )

        curmap = Map()
        curmap.startpos = [int((roomlist[0].width - 1)/2), int((roomlist[0].height - 1)/2)]
        offx = 10
        offy = 10
        curmap.width = 30
        curmap.height = 30

        # set map to all 0s
        curmap.tiles = []
        for y in range(0, curmap.height):
            temp = []
            for x in range(0, curmap.width):
                temp.append(0)
            curmap.tiles.append(temp)

        # add rooms to map
        curmap.startpos[0] = curmap.startpos[0] + offx
        curmap.startpos[1] = curmap.startpos[1] + offy
        for i in range(0, len(roomlist)):
            for y in range(0, roomlist[i].height):
                for x in range(0, roomlist[i].width):
                    curmap.tiles[y + offy][x + offx] = roomlist[i].tiles[y][x]

    return curmap
