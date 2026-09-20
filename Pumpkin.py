# ------ variable definition ------------------------------------------------------------
ws = get_world_size()
dead = 0
# ------ values to input manually  ------------------------------------------------------
pumpksize = 5        # size of the pumpkin area inside each chunk
bordersize = 1       # grass border around each chunk
wide = 2             # number of chunks horizontally
tall = 2             # number of chunks vertically

startrow = 1 #this indicates the row farm starts at (y)
startcol = 1 #this indicates the column farm starts at (x)

# ------ values calculated automatically -----------------------------------------------
chnksize = pumpksize + bordersize   # full chunk size (pumpkin + border)
chnkqty = wide * tall # total number of chunks

farm_width  = wide * chnksize      # total width in cells
farm_height = tall * chnksize      # total height in cells
area = farm_width * farm_height # total farm area

def go(x,y):
	hor = get_pos_x()
	ver = get_pos_y()
	while hor > x: 
		move(West)
		hor -= 1	
	while hor < x: 
		move(East)
		hor += 1
	while ver > y:
		move(South)
		ver -= 1
	while ver < y:
		move(North)
		ver += 1

def gostartchnk():  
	if pumpksize % 2 == 1:   # ----------------- if Pumpkin size is odd
		for i in range(pumpksize):
			move(West)
	else:     #  ------------------------------- if Pumpkin size is even
			move(South)
	for j in range(pumpksize-1):
		move(South)

def next_chunk_up():
	if pumpksize % 2 == 1:   # ----------------- if Pumpkin size is odd
		for i in range(pumpksize):
			move(West)           
		for j in range(bordersize + 1):
			move(North)              
	else:     #  ------------------------------- if Pumpkin size is even
		for i in range(bordersize):
			move(North)

def next_chunk_right():
	global startrow
	if pumpksize % 2 == 1:   # ----------------- if Pumpkin size is odd
		ynow = get_pos_y()
		while ynow != startrow:     
			move(South)
			ynow = get_pos_y()
		for j in range(bordersize):
			move(East)    
	else:     #  ------------------------------- if Pumpkin size is even
		ynow = get_pos_y()
		while ynow != startrow:      
			move(South)
			ynow = get_pos_y() 
		for i in range(chnksize):
			move(East)

def till_right():
	for left in range(pumpksize):
		if get_ground_type() != Grounds.Soil:
			till()
		move(East)

def till_left():
	for r in range(pumpksize):
		move(West)
		if get_ground_type() != Grounds.Soil:
			till()

def till_full_chunk():
	if pumpksize % 2 == 0:   # ----------------- if Pumpkin size is even
		for c in range(pumpksize/2):
			till_right()
			move(North)
			till_left()
			move(North)
	else:   # ---------------------------------- if Pumpkin size is odd 
		for c in range((pumpksize-1)/2):
			till_right()
			move(North)
			till_left()
			move(North)
		till_right()

def pumk():
	plant(Entities.Pumpkin)

def plant_right():
	for left in range(pumpksize):
		pumk()
		move(East)

def plant_left():
	for r in range(pumpksize):
		move(West)
		pumk()

def plant_full_chunk():
	if pumpksize % 2 == 0:   # ----------------- if Pumpkin size is even
		for c in range(pumpksize/2):
			plant_right()
			move(North)
			plant_left()
			move(North)
	else:   # ---------------------------------- if Pumpkin size is odd 
		for c in range((pumpksize-1)/2):
			plant_right()
			move(North)
			plant_left()
			move(North)
		plant_right()

def check_right():
	global dead
	for r in range(pumpksize):
		status = get_entity_type()
		if status == Entities.Dead_Pumpkin:
			harvest()
			pumk()
			dead += 1
		move(East)

def check_left():
	global dead
	for r in range(pumpksize):
		status = get_entity_type()
		if status == Entities.Dead_Pumpkin:
			harvest()
			pumk()
			dead += 1
		move(West)

def initiate(): #__Harvest and replant
	do_a_flip()   # optional
	gostartchnk()
	harvest()
	plant_full_chunk()

def check_full_chunk():
	global dead
	dead = 0
	if pumpksize % 2 == 0:   # ----------------- if Pumpkin size is even
		for c in range(pumpksize/2):
			check_right()
			move(North)
			check_left()
			move(North)
	else:   # ---------------------------------- if Pumpkin size is odd 
		for c in range((pumpksize-1)/2):
			check_right()
			move(North)
			check_left()
			move(North)
		check_right()
#	print(dead) - to check if the counter works properly
	if dead == 0:
		initiate()

clear()
go(startcol, startrow) # come back to start

for row in range(wide):
	for col in range(tall-1):
		till_full_chunk()
		next_chunk_up()
	till_full_chunk()
	next_chunk_right()

go(startcol, startrow) # come back to start

for row in range(wide):
	for col in range(tall-1):
		plant_full_chunk()
		next_chunk_up()
	plant_full_chunk()
	next_chunk_right()

go(startcol, startrow) # come back to start

while True:
    for row in range(wide):
        for col in range(tall - 1):
            check_full_chunk()
            next_chunk_up()
        check_full_chunk()
        next_chunk_right()
    go(startcol, startrow)