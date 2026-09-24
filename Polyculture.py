import FarmingUtils
import FarmingChecks
from Helpers import goto

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
		goto(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			plant_checkerboard_row()
			handled = True

		if not handled:
			spawn_drone(plant_checkerboard_row)

	goto(0, 1)

	while num_drones() > 1:
		pass


def plant_checkerboard_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		if (col + row) % 2 == 0:
			goto(col, row)

			crop = crop_for_tile(col, row)

			if needs_till(crop):
				FarmingUtils.Till()

			plant(crop)


def assign_all_companions():
	for row in range(WORLD_SIZE):
		goto(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			assign_companions_row()
			handled = True

		if not handled:
			spawn_drone(assign_companions_row)

	goto(0, 1)

	while num_drones() > 1:
		pass


def assign_companions_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		if (col + row) % 2 == 0:
			goto(col, row)

			result = get_companion()

			if result != None:
				companion_type, position = result
				cx, cy = position

				goto(cx, cy)

				if get_entity_type() != None:
					harvest()

				if needs_till(companion_type):
					FarmingUtils.Till()

				plant(companion_type)


def harvest_all_primary():
	for row in range(WORLD_SIZE):
		goto(0, row)

		handled = False

		if num_drones() >= SPAWN_LIMIT:
			harvest_row()
			handled = True

		if not handled:
			spawn_drone(harvest_row)

	goto(0, 1)

	while num_drones() > 1:
		pass


def harvest_row():
	row = get_pos_y()

	for col in range(WORLD_SIZE):
		goto(col, row)

		if is_primary_type(get_entity_type()):
			harvest()


if __name__ == "__main__":
	main([Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot])