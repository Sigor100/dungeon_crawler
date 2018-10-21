import pygame
import generation
import os


direct = os.getcwd()
direct = direct[:-4]
os.path.exists(direct)
background = (25, 25, 25)
white = (255, 255, 255)
display_width = 1600
display_height = 800
box_size = 32
hero_x = 0
hero_y = 0
acc_block = 4
hero_id = 5

pygame.init()

img_list = []
for num in range(0, 6):
	path = direct + "/resources/textures/img" + str(num) + ".png"
	img_list.append(pygame.image.load(path))
backpack_background = pygame.image.load(direct + "/resources/backpack.png")

map = 0  # generation.getmap()
"""map = []
b = []
for p in range(0, 15):
	for p1 in range(0, 20):
		b.append(2)
	map.append(b)
	b = []
for p in range(0, 20):
	map[0][p] = 1
for p in range(0, 20):
	map[14][p] = 1"""

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("visuals test")
gameDisplay.fill(background)


def drawscreen(x, y):
	for p in range(0, len(map.tiles), 1):
		for p1 in range(0, len(map.tiles[0]), 1):
			gameDisplay.blit(img_list[map.tiles[p][p1]], (-x + (box_size * p1), -y + (box_size * p)))
	pygame.display.update()
	gameDisplay.fill(background)


def drawbackpack():
	gameDisplay.blit(backpack_background, 0, 0)
	pygame.display.update()


drawbackpack()
