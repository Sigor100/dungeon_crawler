import pygame
import generation
import os

direct = os.getcwd()
# direct = direct[:-4]
os.path.exists(direct)
black = (0, 0, 0)
white = (255, 255, 255)
display_width = 800
display_height = 600
box_size = 32
hero_x = 0
hero_y = 0
acc_block = 4
hero_id = 5

pygame.init()

img_list = []
for num in range(0, 6):
	path = direct + "/resources/img" + str(num) + ".png"
	img_list.append(pygame.image.load(path))

map = generation.getmap()
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
gameDisplay.fill(black)


def drawscreen(x, y, box_size=32):
	for p in range(0, len(map.tiles), 1):
		for p1 in range(0, len(map.tiles[0]), 1):
			gameDisplay.blit(img_list[map.tiles[p][p1]], (-x + (box_size * p1), -y + (box_size * p)))
	pygame.display.update()
	gameDisplay.fill(black)


def whatobject(x, y):
	x = int(x / 32)
	y = int(y / 32)
	return map.tiles[y][x]


def putonmap(x, y):
	global acc_block
	acc_block = map.tiles[int(y / box_size)][int(x / box_size)]
	map.tiles[int(y / box_size)][int(x / box_size)] = hero_id


def takeoffmap(x, y):
	map.tiles[int(y / box_size)][int(x / box_size)] = acc_block


def collisions(x, y, d):
	if d == 0:
		if generation.collidable(whatobject(x, y - box_size)):
			return True
		else:
			return False
	elif d == 1:
		if generation.collidable(whatobject(x + box_size, y)):
			return True
		else:
			return False
	elif d == 2:
		if generation.collidable(whatobject(x, y + box_size)):
			return True
		else:
			return False
	elif d == 3:
		if generation.collidable(whatobject(x - box_size, y)):
			return True
		else:
			return False


"""def collision(x, y, d):
	x = int(x/32)
	y = int(y/32)
	print("sprawdzam: ", x, " ", y, " ",d)
	if d == 0:
		if whatobject(x, y - 1) == 1:
			return False
		else:
			return True
	elif d == 1:
		if whatobject(x + 1, y) == 1:
			return False
		else:
			return True
	elif d == 2:
		if whatobject(x, y + 1) == 1:
			return False
		else:
			return True
	elif d == 3:
		if whatobject(x - 1, y) == 1:
			return False
		else:
			return True"""

# for p in range(0, len(map)):
# print(map)

# drawscreen(0,0,0,0)
# a = input()
"""	clock = pygame.time.Clock()
	pygame.draw.rect(gameDisplay, white, [hero_x, hero_y, block_size, block_size])
	pygame.display.update()
	clock.tick(fps)"""
