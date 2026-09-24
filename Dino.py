from Helpers import goto


def calculate_pair_steps(world_size):
	return ((world_size - 6) // 2 + 2)


def return_and_reset():
	change_hat(Hats.Straw_Hat)
	goto(0, 0)
	change_hat(Hats.Dinosaur_Hat)
	perform_dino_pattern()


def repeat_move(direction, steps):
	for _ in range(steps):
		if not move(direction):
			return_and_reset()
			return False

	return True


def perform_dino_pattern():
	world_size = get_world_size()
	max_index = world_size - 1

	while True:
		# Move to the top-right.
		if not repeat_move(North, max_index):
			return

		if not repeat_move(East, max_index):
			return

		# Move down one row.
		if not repeat_move(South, 1):
			return

		# Sweep the remaining rows.
		for _ in range(calculate_pair_steps(world_size)):
			if not repeat_move(West, max_index - 1):
				return

			if not repeat_move(South, 1):
				return

			if not repeat_move(East, max_index - 1):
				return

			if not repeat_move(South, 1):
				return

		# Return to the western side.
		if not repeat_move(West, max_index):
			return




def main():
	world_size = get_world_size()

# Use an even-sized field for this pattern.
	if world_size % 2 == 1:
		set_world_size(world_size - 1)
		world_size -= 1


	change_hat(Hats.Straw_Hat)
	goto(0, 0)
	change_hat(Hats.Dinosaur_Hat)
	while True:
		perform_dino_pattern()