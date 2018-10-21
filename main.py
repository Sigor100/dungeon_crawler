import pygame
import visuals
import collisions
import generation

pygame.init()

clock = pygame.time.Clock()
box_size = 32
fps = 30

white = (255, 255, 255)
black = (0, 0, 0)

map = generation.getmap()

def gameloop():
	xxx = 0
	yyy = 0

	game_exit = False
	game_over = False
	direction = 0  # 0 = up 1 = right  2= down 	3= left
	hero_x = map.startpos[0]
	hero_y = map.startpos[1]
	hero_x_change = 0
	hero_y_change = 0
	whileinput = 0

	while not game_exit:
		while game_over:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					game_exit = True
					game_over = False
		# INPUT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
			if event.type == pygame.KEYDOWN and whileinput == 0:
				whileinput = 1
				if event.key == pygame.K_a:
					hero_x_change = -box_size
					direction = 3
				if event.key == pygame.K_d:
					hero_x_change = box_size
					direction = 1
				if event.key == pygame.K_w:
					hero_y_change = -box_size
					direction = 0
				if event.key == pygame.K_s:
					hero_y_change = box_size
					direction = 2
			elif event.type == pygame.KEYUP:
				whileinput = 0
				if event.key == pygame.K_a or event.key == pygame.K_d:
					hero_x_change = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					hero_y_change = 0
		collisions.takeoffmap(hero_x, hero_y)
		if visuals.collisions(hero_x, hero_y, direction):
			hero_x = hero_x + hero_x_change
			hero_y = hero_y + hero_y_change
		else:
			print("kolizja")

		collisions.putonmap(hero_x,hero_y)

		# SCREEN
		#visuals.drawscreen(hero_x + xxx, hero_y + yyy, 416 + xxx, 320 + yyy)
		visuals.drawscreen(hero_x-418, hero_y-320)
		clock.tick(fps)

	pygame.quit()
	quit()


gameloop()
