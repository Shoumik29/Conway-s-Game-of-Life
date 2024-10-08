import sys
import random
import pygame
from collections import defaultdict


# Global initializer
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Conway's Game of Life")

OFF_WHITE = (200, 200, 200)
WHITE = (255, 255, 255)
BACKGROUND = (0, 4, 53)

GRID_SIZE = 32   # Use power of 2

clock = pygame.time.Clock()

camera_x, camera_y = 0, 0
drawn_cells = set()



def main():

	global camera_x, camera_y, drawn_cells
	
	run = False
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					#game_of_life()
					run = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				toggle_cells(pygame.mouse.get_pos())
		
		# Handle key presses for camera movement
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			camera_x -= 5
		if keys[pygame.K_RIGHT]:
			camera_x += 5
		if keys[pygame.K_UP]:
			camera_y -= 5
		if keys[pygame.K_DOWN]:
			camera_y += 5
		
		
		if run:
			stable = game_of_life()
			if stable:
				run = False
			
		screen.fill(BACKGROUND)
		
		draw_cells()
		check_zoom_out()
		pygame.display.flip()
					
		clock.tick(60)	
		

def draw_cells():
	global camera_x, camera_y, drawn_cells
	for cell in drawn_cells:
		cell_x, cell_y = cell
		pygame.draw.rect(screen, WHITE, (cell_x - camera_x, cell_y - camera_y, GRID_SIZE, GRID_SIZE))
			

def toggle_cells(mouse_pos):
	global drawn_cells, camera_x, camera_y
	mouse_x, mouse_y = mouse_pos
	grid_x = (mouse_x + camera_x) // GRID_SIZE * GRID_SIZE
	grid_y = (mouse_y + camera_y) // GRID_SIZE * GRID_SIZE
	if (grid_x, grid_y) in drawn_cells:
		drawn_cells.remove((grid_x, grid_y))
	else:
		fill_random_cells((grid_x, grid_y))
		#drawn_cells.add((grid_x, grid_y))
	

def fill_random_cells(center_pos):
	grid_x, grid_y = center_pos
	for _ in range(random.randint(5, 20)):  # Fill 5-10 random cells
		offset_x = random.randint(-2, 2) * GRID_SIZE
		offset_y = random.randint(-2, 2) * GRID_SIZE
		new_cell = (grid_x + offset_x, grid_y + offset_y)
		drawn_cells.add(new_cell)
		

def check_zoom_out():
	global GRID_SIZE, drawn_cells
	total_grids = (HEIGHT * WIDTH) // (GRID_SIZE * GRID_SIZE)
	grid_percentage = (len(drawn_cells) / total_grids) * 100.00
	if grid_percentage > 5:	
		zoom_out()

def zoom_out():
	global GRID_SIZE, camera_x, camera_y, drawn_cells
	new_grid_size = GRID_SIZE // 2
		
	scale_factor = GRID_SIZE / new_grid_size
	
	new_drawn_cells = set()
	for cells in drawn_cells:
		new_x = int(cells[0] / scale_factor)
		new_y = int(cells[1] / scale_factor)
		new_drawn_cells.add((new_x, new_y))
	
	GRID_SIZE = new_grid_size
	drawn_cells = new_drawn_cells
	
	if drawn_cells:
		min_x = min(cell[0] for cell in drawn_cells)
		max_x = max(cell[0] for cell in drawn_cells)
		min_y = min(cell[1] for cell in drawn_cells)
		max_y = max(cell[1] for cell in drawn_cells)
	
	center_x = (max_x + min_x) // 2
	center_y = (max_y + min_y) // 2
	
	camera_x = center_x - WIDTH // 2
	camera_y = center_y - HEIGHT // 2
	
	draw_cells()
	

def game_of_life():
	global GRID_SIZE, drawn_cells
	
	stable = True
	
	cells_neighbors = defaultdict(int)
	new_cells = set()
	
	for cells in drawn_cells:
		neighbor_set = collect_neighbors(cells[0], cells[1])
		for n_cells in neighbor_set:
			cells_neighbors[n_cells] += 1
	
	for cells in cells_neighbors:
		if cells_neighbors[cells] < 2 or cells_neighbors[cells] > 3:
			if cells in drawn_cells:
				stable = False
		else:
			if cells_neighbors[cells] == 3:
				new_cells.add(cells)
				if cells not in drawn_cells:
					stable = False
			else:
				if cells in drawn_cells:
					new_cells.add(cells)
	
	drawn_cells = new_cells
	draw_cells()
	
	return stable					
	

def collect_neighbors(x, y):
	global GRID_SIZE
	
	neighbor_set = set()
	
	neighbor_set.add((x+GRID_SIZE, y))
	neighbor_set.add((x-GRID_SIZE, y))
	neighbor_set.add((x, y+GRID_SIZE))
	neighbor_set.add((x, y-GRID_SIZE))
	neighbor_set.add((x+GRID_SIZE, y+GRID_SIZE))
	neighbor_set.add((x-GRID_SIZE, y-GRID_SIZE))
	neighbor_set.add((x+GRID_SIZE, y-GRID_SIZE))
	neighbor_set.add((x-GRID_SIZE, y+GRID_SIZE))
	
	return neighbor_set
	

if __name__ == '__main__':
	main()
