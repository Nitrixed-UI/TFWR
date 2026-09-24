WORLD_SIZE = get_world_size()
MAX_DRONES = max_drones()
SPAWN_LIMIT = min(WORLD_SIZE, MAX_DRONES)

CROP_CYCLE = []


def main(entities):
	global CROP_CYCLE

	clear()

	CROP_CYCLE = entities

	plant_primary_checkerboard()
	assign_all_companions()
	harvest_all_primary()


def needs_till(entity):
	if entity == Entities.Grass:
		return False
	if entity == Entities.Bush:
		return False
	return True


def is_primary_type(entity):
	for crop in CROP_CYCLE:
		if entity == crop:
			return True

	return False


def crop_for_tile(col, row):
	index = (row * WORLD_SIZE + col) % len(CROP_CYCLE)
	return CROP_CYCLE[index]


def plant_primary_checkerboard():
	for row in range(WORLD_SIZE):
		move_to(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			plant_checkerboard_row()
			handled = True

		if not handled:
			spawn_drone(plant_checkerboard_row)

	move_to(0, 1)

	while num_drones() > 1:
		pass


def plant_checkerboard_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		if (col + row) % 2 == 0:
			move_to(col, row)

			crop = crop_for_tile(col, row)

			if needs_till(crop):
				if get_ground_type() != Grounds.Soil:
					till()

			plant(crop)


def assign_all_companions():
	for row in range(WORLD_SIZE):
		move_to(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			assign_companions_row()
			handled = True

		if not handled:
			spawn_drone(assign_companions_row)

	move_to(0, 1)

	while num_drones() > 1:
		pass


def assign_companions_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		if (col + row) % 2 == 0:
			move_to(col, row)

			result = get_companion()

			if result != None:
				companion_type, position = result
				cx, cy = position

				move_to(cx, cy)

				if get_entity_type() != None:
					harvest()

				if needs_till(companion_type):
					if get_ground_type() != Grounds.Soil:
						till()

				plant(companion_type)


def harvest_all_primary():
	for row in range(WORLD_SIZE):
		move_to(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			harvest_row()
			handled = True

		if not handled:
			spawn_drone(harvest_row)

	move_to(0, 1)

	while num_drones() > 1:
		pass


def harvest_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		move_to(col, row)

		if is_primary_type(get_entity_type()):
			harvest()


def move_to(x, y):
	half = WORLD_SIZE / 2

	while True:
		px = get_pos_x()
		py = get_pos_y()

		if px == x and py == y:
			return

		dx = x - px
		dy = y - py

		if dx > 0:
			if dx > half:
				move(West)
			else:
				move(East)
		elif dx < 0:
			if abs(dx) > half:
				move(East)
			else:
				move(West)

		if dy > 0:
			if dy > half:
				move(South)
			else:
				move(North)
		elif dy < 0:
			if abs(dy) > half:
				move(North)
			else:
				move(South)


if __name__ == "__main__":
	main([Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot])