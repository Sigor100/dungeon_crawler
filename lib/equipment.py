import pygame
import os


pygame.init()

direct = os.getcwd()
direct = direct[:-4]

file_list = []
equipment_list = []


class Item:
	def __init__(self, id, type, name):
		self.id = id
		self.type = type  # 0 = weapon	1 = potion
		self.name = name


class Weapon(Item):
	def __init__(self, id, name, damage, durability, crit_damage, crit_chance):
		#Item.__init__(id,0 , name)
		self.id = id
		self.type = 0  # 0 = weapon	1 = potion
		self.name = name
		self.damage = damage
		self.durability = durability
		self.crit_damage = crit_damage
		self.crit_chance = crit_chance

	def getstats(self, n):
		if n == 0:
			return [self.damage, self.durability, self.crit_damage, self.crit_chance]
		elif n == 1:
			return self.damage
		elif n == 2:
			return self.durability
		elif n == 3:
			return self.crit_damage
		elif n == 4:
			return self.crit_chance


for num in range(0, 3):
	equipment_file = open(direct + "/resources/items/item" + str(num) + ".txt")
	equipment_file = list(equipment_file)
	equipment_file = str(equipment_file)
	equipment_file = list(equipment_file)
	# print(equipment_file)
	file_list.append(equipment_file)

for p in range(0, len(file_list), 1):
	file_list[p] = file_list[p][2:]
	file_list[p] = file_list[p][:-2]
# print(file_list)

end = False
p2 = 0
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
		h_list2.append("".join(h_list))  # todo skonczyc itemy
		h_list = []
		equipment_list.append(h_list2)
		h_list2 = []
print(equipment_list)
for p in range(0, len(equipment_list)):
	print(equipment_list[p][1])
	equipment_list[p] = Weapon(p, equipment_list[p][1], equipment_list[p][2], equipment_list[p][3], equipment_list[p][4], equipment_list[p][5]) # todo tu skonczylem

print(equipment_list[0].name)