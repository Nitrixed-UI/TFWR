import FarmingUtils
import FarmingChecks
from Helpers import goto

WORLD_SIZE = get_world_size()
MAX_DRONES = max_drones()
SPAWN_LIMIT = min(WORLD_SIZE, MAX_DRONES)

row_results = []  # filled per-row by parallel scan; row_results[row] = [[col, petals], ...]


def main():
	plant_all_sunflowers()
	pet_the_piggy()
	pet_the_piggy()
	pet_the_piggy()
	pet_the_piggy()
	pet_the_piggy()
	sunflowers = scan_all_sunflowers()  # dict: (col, row) -> petal count
	harvest_priority_sequential(sunflowers)
	harvest_tail_parallel()


def plant_all_sunflowers():
	global WORLD_SIZE
	global SPAWN_LIMIT
	for row in range(WORLD_SIZE):
		goto(0, row)

		handled = False
		if num_drones() >= SPAWN_LIMIT:
			plant_row()
			handled = True

		if not handled:
			spawn_drone(plant_row)

	goto(0, 1)
	while num_drones() > 1:
		pass


def plant_row():
	global WORLD_SIZE
	row = get_pos_y()
	for col in range(WORLD_SIZE):
		goto(col, row)
		FarmingUtils.Till()
		if not FarmingChecks.is_over(Entities.Sunflower):
			plant(Entities.Sunflower)


def scan_all_sunflowers():
	global WORLD_SIZE
	global SPAWN_LIMIT
	global row_results

	row_results = []
	for row in range(WORLD_SIZE):
		row_results.append([])

	for row in range(WORLD_SIZE):
		goto(0, row)

		handled = False
		if num_drones() >= SPAWN_LIMIT:
			scan_row()
			handled = True

		if not handled:
			spawn_drone(scan_row)

	goto(0, 1)
	while num_drones() > 1:
		pass

	sunflowers = {}
	for row in range(WORLD_SIZE):
		for entry in row_results[row]:
			col = entry[0]
			petals = entry[1]
			sunflowers[(col, row)] = petals

	return sunflowers


def scan_row():
	global WORLD_SIZE
	global row_results
	row = get_pos_y()
	for col in range(WORLD_SIZE):
		goto(col, row)
		if FarmingChecks.is_over(Entities.Sunflower):
			petals = measure()
			row_results[row].append([col, petals])


def find_max_position(sunflowers, harvested):
	# Pure Python dict scan, costs nothing -- no game actions.
	best_pos = None
	best_petals = -1
	for pos in sunflowers:
		if pos not in harvested:
			petals = sunflowers[pos]
			if petals > best_petals:
				best_petals = petals
				best_pos = pos
	return best_pos


def harvest_priority_sequential(sunflowers):
	# While at least ten remain, re-derive the current maximum after every
	# harvest so the largest remaining sunflower gets the bonus.
	harvested = set()
	remaining = len(sunflowers)

	while remaining >= 10:
		pos = find_max_position(sunflowers, harvested)
		if pos == None:
			break
		goto(pos[0], pos[1])
		harvest()
		harvested.add(pos)
		remaining -= 1


def harvest_tail_parallel():
	# Fewer than 10 remain -- bonus is impossible no matter the order,
	# so it's safe to sweep whatever's left in parallel.
	global WORLD_SIZE
	global SPAWN_LIMIT
	for row in range(WORLD_SIZE):
		goto(0, row)

		handled = False
		if num_drones() >= SPAWN_LIMIT:
			harvest_tail_row()
			handled = True

		if not handled:
			spawn_drone(harvest_tail_row)

	goto(0, 1)
	while num_drones() > 1:
		pass


def harvest_tail_row():
	global WORLD_SIZE
	row = get_pos_y()
	for col in range(WORLD_SIZE):
		goto(col, row)
		if FarmingChecks.is_over(Entities.Sunflower):
			harvest()


if __name__ == "__main__":
	clear()
	main()