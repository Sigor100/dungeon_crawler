import random as r
import pygame as py
import collisions as c
import entities as e
import generation as g
import settings as s
import visuals as v

py.init()
g.init()
e.init()
e.Player()
v.init()

box_size = 32

white = (255, 255, 255)
black = (0, 0, 0)


def gameloop():
    game_exit = False
    game_over = False
    direction = [0, 0]  # 0 - y axis; 1 - z axis
    cam_dir = [0, 0]
    cam_offset = [0, 0]
    clock = py.time.Clock()

    turn = True  # true = my turn   false = enemy turn

    while not game_exit:
        while game_over:
            for event in py.event.get():
                if event.type == py.KEYDOWN:
                    game_exit = True
                    game_over = False
        # INPUTd
        temp = 0
        while temp == 0:
            for event in py.event.get():
                if event.type == py.QUIT:
                    game_exit = True
                    break
                elif event.type == py.KEYDOWN:
                    # begin player movement
                    if event.key == py.K_w:
                        turn = False
                        direction[0] -= 1
                    elif event.key == py.K_s:
                        turn = False
                        direction[0] += 1
                    elif event.key == py.K_a:
                        turn = False
                        direction[1] -= 1
                    elif event.key == py.K_d:
                        turn = False
                        direction[1] += 1

                    # begin camera movement
                    elif event.key == py.K_RIGHT:
                        cam_dir[0] += box_size
                    elif event.key == py.K_LEFT:
                        cam_dir[0] -= box_size
                    elif event.key == py.K_UP:
                        cam_dir[1] -= box_size
                    elif event.key == py.K_DOWN:
                        cam_dir[1] += box_size

                    # reset camera
                    elif event.key == py.K_SPACE:
                        cam_offset = [0, 0]

                    # skip turn
                    elif event.key == py.K_q:
                        turn = False

                    # pathfinding test
                    elif event.key == py.K_p:
                        print("burza")
                        spos = [0, 0]
                        epos = [0, 0]
                        while True:
                            spos[0] = r.randint(0, g.curmap.width - 1)
                            spos[1] = r.randint(0, g.curmap.height - 1)
                            epos[0] = r.randint(0, g.curmap.width - 1)
                            epos[1] = r.randint(0, g.curmap.height - 1)
                            if g.curmap.tiles[spos[1]][spos[0]] == 2 and g.curmap.tiles[epos[1]][epos[0]] == 2:
                                print(spos)
                                print(epos)
                                g.curmap.tiles[spos[1]][spos[0]] = 4
                                g.curmap.tiles[epos[1]][epos[0]] = 4
                                break
                        heropath = c.getpath(spos, epos)
                        print(heropath)

                    # todo: eq/backpack window here
                    # elif event.key == py.K_e:

                elif event.type == py.KEYUP:
                    # stop character
                    if event.key == py.K_w:
                        direction[0] += 1
                    if event.key == py.K_s:
                        direction[0] -= 1
                    if event.key == py.K_a:
                        direction[1] += 1
                    if event.key == py.K_d:
                        direction[1] -= 1

                    # stop camera
                    if event.key == py.K_RIGHT:
                        cam_dir[0] -= box_size
                    if event.key == py.K_LEFT:
                        cam_dir[0] += box_size
                    if event.key == py.K_UP:
                        cam_dir[1] += box_size
                    if event.key == py.K_DOWN:
                        cam_dir[1] -= box_size

            if game_exit:
                break
            temp = 1

        # move the player
        if not direction == [0, 0]:
            e.player.move([direction[1], direction[0]])

        # move the camera
        if not cam_dir == [0, 0]:
            cam_offset[0] += cam_dir[0]
            cam_offset[1] += cam_dir[1]

        # do turn shit
        if not turn:  # and len(e.alive_enemies_list) > 0:
            # print("enemy turn")
            # print("alive: ", len(e.alive_enemies_list))
            if r.randint(0, 100) < 10:
                while True:
                    x = r.randint(0, g.curmap.width - 1)
                    y = r.randint(0, g.curmap.height - 1)
                    if g.tilesprot[g.curmap.tiles[y][x]].name == 'floor':
                        break
                e.Entity(1, x, y)
            e.turn()  # todo: still working on it
            turn = True
        # SCREEN
        v.drawscreen(e.player.x * box_size + box_size / 2 + cam_offset[0] - s.display_width / 2,
                     e.player.y * box_size + box_size / 2 + cam_offset[1] - s.display_height / 2)
        clock.tick(s.fps)
    py.quit()
    quit()


gameloop()
