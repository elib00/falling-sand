import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 40
GRID_HEIGHT = 40
CELL_SIZE = 16
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 30

# Colors
BLACK = (0, 0, 0)
SAND_COLOR = (194, 178, 128)
EMPTY_COLOR = BLACK

#Essential Matrices
STATE_MATRIX = [[-1] * GRID_WIDTH for size in range(GRID_HEIGHT)]

TRANSITION_MATRIX = [
    [1, 2, -1, -1, -1, -1, -1], #for the stable/resting state (0)
    [1, 2, -1, -1, -1, -1, -1], #for the falling state (1),
    [-1, -1, 1, 1, 1, 3, -1], #for the pending state (2)
    [-1, -1, -1, -1, -1, -1, 0] #for the blocked state (3)
]

CLOCK = pygame.time.Clock()
# FRAME_COUNTER = 0
# FRAME_INTERVAL = 2

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cellular Automaton (FSM) - Simple Falling Sand Simulator")

# Create the grid (10x10, filled with empty cells represented by 0)
GRID = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = SAND_COLOR if GRID[y][x] == 1 else EMPTY_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to add sand at a specific location
def add_sand(x, y):
    if GRID[y][x] == 0:
        GRID[y][x] = 1
        STATE_MATRIX[y][x] = 0 #resting

# Falling logic for the sand
def update_sand():
    for y in range(GRID_HEIGHT - 1, -1, -1):
        for x in range(GRID_WIDTH):
            condition = -1
            
            if GRID[y][x] != 0:
                condition = determine_condition(y, x)
            
                if condition == 0 and STATE_MATRIX[y][x] == 1: #falling, move sa below
                    state = STATE_MATRIX[y][x]
                    GRID[y][x] = 0 #the last location kay i empty na nato
                    GRID[y + 1][x] = 1 #balhin na sa new loc, which is down
                    STATE_MATRIX[y][x] = -1 #meaning ra ana wala ta ga keep track ana nga cell
                    STATE_MATRIX[y + 1][x] = state
                elif condition == 2 and STATE_MATRIX[y][x] == 1: #meaning pending to falling, move left
                    state = STATE_MATRIX[y][x]
                    GRID[y][x] = 0
                    GRID[y + 1][x - 1] = 1
                    STATE_MATRIX[y][x] = -1
                    STATE_MATRIX[y + 1][x - 1] = state
                elif condition == 3 and STATE_MATRIX[y][x] == 1: #meaning pending to falling, move right
                    state = STATE_MATRIX[y][x]
                    GRID[y][x] = 0
                    GRID[y + 1][x + 1] = 1
                    STATE_MATRIX[y][x] = -1
                    STATE_MATRIX[y + 1][x + 1] = state
                elif condition == 4 and STATE_MATRIX[y][x] == 1: #meaning pending to falling, move left or right
                    state = STATE_MATRIX[y][x]
                    GRID[y][x] = 0
                        
                    #1 - left, 2 - right
                    random_number = random.randint(1, 2)
                    
                    if random_number == 1:
                        GRID[y + 1][x - 1] = 1
                        STATE_MATRIX[y][x] = -1
                        STATE_MATRIX[y + 1][x - 1] = state
                    elif random_number == 2:
                        GRID[y + 1][x + 1] = 1
                        STATE_MATRIX[y][x] = -1
                        STATE_MATRIX[y + 1][x + 1] = state  
                elif condition == 5 and STATE_MATRIX[y][x] == 3: #blocked, transition to resting
                    condition = 6 #condition 6 is for settling to resting state
                    current_state = STATE_MATRIX[y][x]
                    STATE_MATRIX[x][y] = TRANSITION_MATRIX[current_state][condition] #nahimo na siya nga resting

def determine_condition(row: int, col: int):
    condition = -1
    if row + 1 < GRID_HEIGHT: #check if naay valid nga lower cell
        if GRID[row + 1][col] == 0: # ilalom kay free
            condition = 0
            current_state = STATE_MATRIX[row][col]
            STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition]
            return condition
        elif GRID[row + 1][col] == 1: # ilalom kay blocked
            #check if the bottom left or bottom right kay free cell
            condition = 1
            current_state = STATE_MATRIX[row][col]
            STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to pending

            is_left_free, is_right_free = False, False 
            if row + 1 < GRID_HEIGHT and col - 1 >= 0: #check if naay valid nga lower left cell
                if GRID[row + 1][col - 1] == 0: #free si left cell
                    is_left_free = True

            if row + 1 < GRID_HEIGHT and col + 1 < GRID_WIDTH: #check if naay valid nga lower right cell
                if GRID[row + 1][col + 1] == 0:
                    is_right_free = True         
                        
            #check asa moadto next left ba or right
            if is_left_free and not is_right_free:
                condition = 2 #adto left; 
                current_state = STATE_MATRIX[row][col]
                STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to falling - left
                return condition
            if not is_left_free and is_right_free:
                condition = 3 #adto right
                current_state = STATE_MATRIX[row][col]
                STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to falling - right (galibog nako)
                return condition
            if is_left_free and is_right_free:
                condition = 4 #choose at random
                current_state = STATE_MATRIX[row][col]
                STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to falling - both directions
                return condition
            if not is_left_free and not is_right_free:
                condition = 5 #meaning ani naa natas kinailaloman
                current_state = STATE_MATRIX[row][col]
                STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to blocked
                return condition
    else:
        conditions = [1, 5, 6]
        for condition in conditions:
            current_state = STATE_MATRIX[row][col]
            STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition]
    

def main():
    is_running = True
    while is_running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            #comment this out if ganahan ka magdrop og sands based sa click
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_x, mouse_y = pygame.mouse.get_pos()
            #     grid_x = mouse_x // CELL_SIZE
            #     grid_y = mouse_y // CELL_SIZE
            #     add_sand(grid_x, grid_y)
           
        # FRAME_COUNTER += 1
        
        # if FRAME_COUNTER % FRAME_INTERVAL == 0:
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     grid_x = mouse_x // CELL_SIZE
        #     grid_y = mouse_y // CELL_SIZE
        #     add_sand(grid_x, grid_y)
            
        #continuous dropping of sands
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // CELL_SIZE
        grid_y = mouse_y // CELL_SIZE
        add_sand(grid_x, grid_y)
        
        update_sand()
        draw_grid()

        # Update the display
        pygame.display.flip()
        CLOCK.tick(FPS)
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()