import os
import generation


class Enemie():
	def __init__(self, id, type, name, damage, hp, drop_min, drop_max):
		self.id = id
		self.type = type  # 0 = melee	1 = ranged  2 = both
		self.name = name
		self.damage = damage
		self.hp = hp
		self.drop_min = drop_min
		self.drop_max = drop_max


def init():
	direct = os.getcwd()
	direct = direct[:-4]

	enemie_file = []
	file_list = []
	enemie_list = []


	for p in range(0, 1):
		enemie_file = open(direct + "/resources/enemies/enemie" + str(p) + ".txt")
		enemie_file = list(enemie_file)
		enemie_file = str(enemie_file)
		enemie_file = list(enemie_file)
		file_list.append(enemie_file)

	for p in range(0, len(file_list), 1):
		file_list[p] = file_list[p][2:]
		file_list[p] = file_list[p][:-2]

	h_list = []
	h_list2 = []

	for p in range(0, len(file_list), 1):
		if file_list[p][0] == "0":
			for p1 in range(0, len(file_list[p])):
				if file_list[p][p1] != " ":
					h_list.append(file_list[p][p1])
				else:
					h_list2.append("".join(h_list))
					h_list = []
			h_list2.append("".join(h_list))
			h_list = []
			enemie_list.append(h_list2)
			h_list2 = []
	print(enemie_list)
	for p in range(1, len(enemie_list)):
		print(enemie_list[p][1])
		enemie_list[p] = Enemie(enemie_list[p][0], enemie_list[p][1], enemie_list[p][2], enemie_list[p][3],
								enemie_list[p][4], enemie_list[p][5], enemie_list[p][6])
