import pygame
import generation

map = generation.getmap()

box_size = 32
hero_id = 5
acc_block = 4

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

def putonmap(x, y):
	global acc_block
	acc_block = map.tiles[int(y / box_size)][int(x / box_size)]
	map.tiles[int(y / box_size)][int(x / box_size)] = hero_id


def takeoffmap(x, y):
	map.tiles[int(y / box_size)][int(x / box_size)] = acc_block

def whatobject(x, y):
	x = int(x / 32)
	y = int(y / 32)
	return map.tiles[y][x]