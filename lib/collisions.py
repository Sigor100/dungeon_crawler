import generation
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

disablecollisions = False  # set to true for debug
pathfindingdebug = True

dirx = (0, 1, 1, 1, 0, -1, -1, -1)
diry = (-1, -1, 0, 1, 1, 1, 0, -1)


def collisions(x, y, d):
    a = generation.curmap.tiles[int((y + d[1])/32)][int((x + d[0])/32)]
    if generation.tilesprot[a].collision > 0 or disablecollisions:
        return True
    else:
        return False


def getpath(spos, epos):
    generation.curmap.generategrid()
    print(spos, epos)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(generation.curmap.grid.node(spos[0], spos[1]),
                                  generation.curmap.grid.node(epos[0], epos[1]),
                                  generation.curmap.grid)
    if pathfindingdebug:
        print(runs)
        print(path)
    return path[1:-1]
