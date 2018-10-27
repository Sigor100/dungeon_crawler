import pygame
import visuals
import collisions as c
import generation
import random


pygame.init()

clock = pygame.time.Clock()
box_size = 32
fps = 30

curmap = generation.getmap()
white = (255, 255, 255)
black = (0, 0, 0)


def gameloop():
    game_exit = False
    game_over = False
    direction = [0, 0]  # 0 - y axis; 1 - z axis
    hero_x = curmap.startpos[0]
    hero_y = curmap.startpos[1]

    hero_x = 32 * curmap.startpos[0]
    hero_y = 32 * curmap.startpos[1]
    camera_x_change = 0
    camera_y_change = 0

    turn = True # true = my turn   false = enemy turn
    #

    while not game_exit:
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game_exit = True
                    game_over = False
        # INPUT
        while turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        turn = False
                        direction[0] -= 32
                    if event.key == pygame.K_s:
                        turn = False
                        direction[0] += 32
                    if event.key == pygame.K_a:
                        turn = False
                        direction[1] -= 32
                    if event.key == pygame.K_d:
                        turn = False
                        direction[1] += 32

                    if event.key == pygame.K_RIGHT:
                        turn = False
                        camera_x_change = camera_x_change + box_size
                    if event.key == pygame.K_LEFT:
                        turn = False
                        camera_x_change = camera_x_change - box_size
                    if event.key == pygame.K_UP:
                        turn = False
                        camera_y_change = camera_y_change - box_size
                    if event.key == pygame.K_DOWN:
                        turn = False
                        camera_y_change = camera_y_change + box_size
                    if event.key == pygame.K_SPACE:
                        turn = False
                        camera_x_change = 0
                        camera_y_change = 0

                    if event.key == pygame.K_z:
                        print(visuals.get_discoverymap())
                    if event.key == pygame.K_p:
                        print("burza")
                        spos = [0, 0]
                        epos = [0, 0]
                        while True:
                            spos[0] = random.randint(0, curmap.width - 1)
                            spos[1] = random.randint(0, curmap.height - 1)
                            epos[0] = random.randint(0, curmap.width - 1)
                            epos[1] = random.randint(0, curmap.height - 1)
                            if curmap.tiles[spos[1]][spos[0]] == 2 and curmap.tiles[epos[1]][epos[0]] == 2:
                                print(spos)
                                print(epos)
                                curmap.tiles[spos[1]][spos[0]] = 4
                                curmap.tiles[epos[1]][epos[0]] = 4
                                break
                        heropath = c.getpath(spos, epos)
                        print(heropath)
                # elif event.key == pygame.K_e:
                # todo: eq/backpack window here
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        direction[0] += 32
                    if event.key == pygame.K_s:
                        direction[0] -= 32
                    if event.key == pygame.K_a:
                        direction[1] += 32
                    if event.key == pygame.K_d:
                        direction[1] -= 32

            if game_exit:
                break
        c.takeoffmap(hero_x, hero_y)
        if c.collisions(hero_x, hero_y, direction):
            hero_x = hero_x + direction[1]
            hero_y = hero_y + direction[0]
        #else:
            # print("kolizja")
        c.putonmap(hero_x, hero_y)
        if turn == False:
            #print("twoja kolej")
            turn = True
        # SCREEN
        visuals.countplayervisibility(hero_x, hero_y, 1)
        visuals.drawscreen((hero_x - 800) + camera_x_change, (hero_y - 400) + camera_y_change)
        clock.tick(fps)

    pygame.quit()
    quit()


gameloop()
