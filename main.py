import pygame
import visuals
import collisions as c
import generation


pygame.init()

clock = pygame.time.Clock()
box_size = 32
fps = 30

map = generation.getmap()
white = (255, 255, 255)
black = (0, 0, 0)


def gameloop():
	game_exit = False
	game_over = False
	direction = [0, 0]  # 0 - y axis; 1 - z axis
	hero_x = map.startpos[0]
	hero_y = map.startpos[1]

	hero_x = 32 * map.startpos[0]
	hero_y = 32 * map.startpos[1]
	hero_x_change = 0
	hero_y_change = 0
	#

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
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					direction[0] -= 32
				if event.key == pygame.K_s:
					direction[0] += 32
				if event.key == pygame.K_a:
					direction[1] -= 32
				if event.key == pygame.K_d:
					direction[1] += 32
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
		c.takeoffmap(hero_x, hero_y)
		if c.collisions(hero_x, hero_y, direction):
			hero_x = hero_x + direction[1]
			hero_y = hero_y + direction[0]
		else:
			print("kolizja")
		c.putonmap(hero_x, hero_y)

		# SCREEN
		visuals.drawscreen(hero_x - 418, hero_y - 320)
		clock.tick(fps)

	pygame.quit()
	quit()


gameloop()
