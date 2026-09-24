WORLD_SIZE = get_world_size()
MAX_DRONES = max_drones()
SPAWN_LIMIT = min(WORLD_SIZE, MAX_DRONES)  # never try to spawn more than the cap allows


def main():
	clear()
	plant_and_sort_all_rows()
	sort_all_columns()
	harvest()


def plant_and_sort_all_rows():
	global WORLD_SIZE
	global SPAWN_LIMIT
	for row in range(WORLD_SIZE):
		move_to(0, row)

		handled = False
		if num_drones() >= SPAWN_LIMIT:
			pas_current_row()
			handled = True

		if not handled:
			spawn_drone(pas_current_row)

	move_to(0, 1)
	while num_drones() > 1:
		pass


def pas_current_row():
	global WORLD_SIZE
	row = get_pos_y()
	for col in range(WORLD_SIZE):
		move_to(col, row)
		till()
		plant(Entities.Cactus)
		insertion_sort_row_step()


def insertion_sort_row_step():
	# The drone's own value travels with it through each swap+move, so we only
	# need to measure() once up front instead of every iteration.
	current = measure()
	while get_pos_x() > 0:
		if current < measure(West):
			swap(West)
			move(West)
			# current is unchanged: after swap(West), West's cell now holds
			# our original value, and we just moved onto it.
		else:
			break


def sort_all_columns():
	global WORLD_SIZE
	global SPAWN_LIMIT
	for col in range(WORLD_SIZE):
		move_to(col, 1)

		handled = False
		if num_drones() >= SPAWN_LIMIT:
			sort_current_column()
			handled = True

		if not handled:
			spawn_drone(sort_current_column)

	while num_drones() > 1:
		pass


def sort_current_column():
	# Left as-is: the recursive descend/compare/ascend pattern here is
	# non-obvious, and recursion depth is bounded by WORLD_SIZE (cheap),
	# so flattening it risks breaking correctness for no real gain.
	global WORLD_SIZE
	while get_pos_y() < (WORLD_SIZE - 1):
		insertion_sort_column_step()
	insertion_sort_column_step()


def insertion_sort_column_step():
	if get_pos_y() == 0:
		move(North)
		return

	current = measure()
	south = measure(South)
	if current != None and south != None and current < south:
		swap(South)
		if get_pos_y() > 1:
			move(South)
			insertion_sort_column_step()
			return

	move(North)


def move_to(x, y):
	global WORLD_SIZE
	half = WORLD_SIZE / 2

	while True:
		px, py = get_pos_x(), get_pos_y()
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
	clear()
	main()
	harvest()