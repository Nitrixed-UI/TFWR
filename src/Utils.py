# Utils file

current_Size = get_world_size()


#           [Entity, needs_till()]
Types = {
     "Bush": [Entities.Bush, False],
     "Cactus": [Entities.Cactus, True],
     "Carrot": [Entities.Carrot, True],
     "Pumpkin": [Entities.Pumpkin, True],
     "Grass": [Entities.Grass, False],
     "Sunflower": [Entities.Sunflower, True],
     "Tree": [Entities.Tree, False],
}

def is_odd(value):
	return value % 2 == 1

def is_even(value):
	return value % 2 == 0

def goto(x, y):
    
    x_pos = get_pos_x()
    y_pos = get_pos_y()

    dx = x - x_pos
    dy = y - y_pos

    while dx != 0:
        if dx > 0:
            move(East)
            dx -= 1
        else:
            move(West)
            dx += 1

    while dy != 0:
        if dy > 0:
            move(North)
            dy -= 1
        else:
            move(South)
            dy += 1

def get_distance_to(x, y):
    x_pos = get_pos_x()
    y_pos = get_pos_y()

    dx = x - x_pos
    dy = y - y_pos
    
    return (dx, dy)

def plant_all(type):
    plant_type = Types[type][0]
    needs_till = Types[type][1]
    for x in range(current_Size):
        for y in range(current_Size):
            goto(x, y)
            if needs_till:
                till()
            plant(plant_type)

def harvest_all_of_type(type):
    plant_type = Types[type][0]
    for x in range(current_Size):
        for y in range(current_Size):
            goto(x, y)
            if get_entity_type() == plant_type:
                harvest()

def harvest_all():
    for x in range(current_Size):
        for y in range(current_Size):
            goto(x, y)
            harvest()

def plant_at(type, x, y):
    plant_type = Types[type][0]
    needs_till = Types[type][1]
    goto(x, y)
    if needs_till:
        till()
    plant(plant_type)

def harvest_at(x, y):
    goto(x, y)
    harvest()

def moveToNextTile(dir):
	bX = get_world_size() #Farm width (x Boundary)
	bY = bX #Farm height (y Boundary)
	cX = get_pos_x() #Current X position
	cY = get_pos_y() #Current Y position
	if (dir==East):
		if (cX+1==bX):
			dir=North
	elif (dir==West):
		if (cX==0):
			dir=North
	elif (dir==North):
		if (cX+1==bX):
			dir=West
		elif (cX==0):
			dir=East
			
	move(dir)
	return dir