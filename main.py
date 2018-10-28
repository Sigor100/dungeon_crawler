import pygame as py
import visuals as v
import collisions as c
import generation as g
import random as r
import enemies as e

py.init()

clock = py.time.Clock()
box_size = 32
fps = 30

curmap = g.getmap()
white = (255, 255, 255)
black = (0, 0, 0)


def gameloop():
    game_exit = False
    game_over = False
    direction = [0, 0]  # 0 - y axis; 1 - z axis
    # hero_x = curmap.startpos[0]
    # hero_y = curmap.startpos[1]

    hero_x = 32 * curmap.startpos[0]
    hero_y = 32 * curmap.startpos[1]
    camera_x = 0
    camera_y = 0
    camera_x_change = 0
    camera_y_change = 0

    turn = True  # true = my turn   false = enemy turn

    e.init()

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
                    if event.key == py.K_w:
                        turn = False
                        direction[0] -= 32
                    if event.key == py.K_s:
                        turn = False
                        direction[0] += 32
                    if event.key == py.K_a:
                        turn = False
                        direction[1] -= 32
                    if event.key == py.K_d:
                        turn = False
                        direction[1] += 32

                    if event.key == py.K_RIGHT:
                        camera_x_change = camera_x_change + box_size
                    if event.key == py.K_LEFT:
                        camera_x_change = camera_x_change - box_size
                    if event.key == py.K_UP:
                        camera_y_change = camera_y_change - box_size
                    if event.key == py.K_DOWN:
                        camera_y_change = camera_y_change + box_size
                    if event.key == py.K_SPACE:
                        camera_x = 0
                        camera_y = 0
                    if event.key == py.K_q:
                        turn = False
                    if event.key == py.K_z:
                        # print(v.get_discoverymap())
                        # print(len(e.alive_enemies_list))
                        print(hero_x / 32, hero_y / 32)
                        #print(len(e.alive_enemies_list))
                    if event.key == py.K_p:
                        print("burza")
                        spos = [0, 0]
                        epos = [0, 0]
                        while True:
                            spos[0] = r.randint(0, curmap.width - 1)
                            spos[1] = r.randint(0, curmap.height - 1)
                            epos[0] = r.randint(0, curmap.width - 1)
                            epos[1] = r.randint(0, curmap.height - 1)
                            if curmap.tiles[spos[1]][spos[0]] == 2 and curmap.tiles[epos[1]][epos[0]] == 2:
                                print(spos)
                                print(epos)
                                curmap.tiles[spos[1]][spos[0]] = 4
                                curmap.tiles[epos[1]][epos[0]] = 4
                                break
                        heropath = c.getpath(spos, epos)
                        print(heropath)
                # elif event.key == py.K_e:
                # todo: eq/backpack window here
                elif event.type == py.KEYUP:
                    if event.key == py.K_w:
                        direction[0] += 32
                    if event.key == py.K_s:
                        direction[0] -= 32
                    if event.key == py.K_a:
                        direction[1] += 32
                    if event.key == py.K_d:
                        direction[1] -= 32
                    if event.key == py.K_RIGHT:
                        camera_x_change = camera_x_change - box_size
                    if event.key == py.K_LEFT:
                        camera_x_change = camera_x_change + box_size
                    if event.key == py.K_UP:
                        camera_y_change = camera_y_change + box_size
                    if event.key == py.K_DOWN:
                        camera_y_change = camera_y_change - box_size

            if game_exit:
                break
            temp = 1
        c.takeoffmap(hero_x, hero_y)
        if c.collisions(hero_x, hero_y, direction):
            hero_x = hero_x + direction[1]
            hero_y = hero_y + direction[0]
        camera_x = camera_x + camera_x_change
        camera_y = camera_y + camera_y_change
        # else:
        # print("kolizja")
        c.putonmap(hero_x, hero_y)
        if not turn:  # and len(e.alive_enemies_list) > 0:
            #print("enemy turn")
            # print("alive: ", len(e.alive_enemies_list))
            if r.randint(0, 100) < 35:
                e.spawn_enemy(-1, -1, 1, 1)
            e.enemy_turn(hero_x, hero_y)  # todo: still working on it
            turn = True
        # SCREEN
        v.countplayervisibility(hero_x, hero_y)
        v.drawscreen((hero_x - 800) + camera_x, (hero_y - 400) + camera_y)
        clock.tick(fps)

    py.quit()
    quit()


gameloop()
