import pygame
import visuals
import generation


pygame.init()

clock = pygame.time.Clock()
box_size = 32
fps = 30

white = (255, 255, 255)
black = (0, 0, 0)


def gameloop():
	xxx = 0
	yyy = 0

	game_exit = False
	game_over = False
	direction = 0  # 0 = gora 1 = prawo  2= dol 	3= lewo
	hero_x = 32 * 10
	hero_y = 32 * 10
	hero_x_change = 0
	hero_y_change = 0

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
				if event.key == pygame.K_a or event.key == pygame.K_d:
					hero_x_change = 0
				if event.key == pygame.K_w or event.key == pygame.K_s:
					hero_y_change = 0

		# if visuals.whatobject()
		"""if not visuals.collision(hero_y, hero_y, direction):
			hero_y_change = 0
			hero_x_change = 0
		else:
			print(hero_x)"""
		visuals.takeoffmap(hero_x, hero_y)
		if visuals.collisions(hero_x, hero_y, direction):
			hero_x = hero_x + hero_x_change
			hero_y = hero_y + hero_y_change
		else:
			print("kolizja")

		visuals.putonmap(hero_x,hero_y)

		# EKRAN
		#visuals.drawscreen(hero_x + xxx, hero_y + yyy, 416 + xxx, 320 + yyy)
		visuals.drawscreen(hero_x-418, hero_y-320)
		clock.tick(fps)

	pygame.quit()
	quit()


gameloop()
