import generation

disablecollisions = False  # set to true for debug

box_size = 32
hero_id = 5
acc_block = 4
map = generation.getmap()


def collisions(x, y, d):
	if generation.collidable(whatobject(x + d[1], y + d[0])) or disablecollisions:
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
