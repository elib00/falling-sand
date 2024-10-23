"""
    --- CELLULAR AUTOMATA ---
    - Basic Falling Sand Simulation (Command-Line Interface Version) by Joshua F. Napinas
"""
import random
    
# 0 kay empty cell, 1 kay taken cell

N = 0
while True:
    try:
        N = int(input("Enter N: "))
        break
    except ValueError:
        print("Invalid number, please try again.")
    

GRID = [[0] * N for size in range(N)] #creating the grid
# NEXT_GRID = [[0] * N for size in range(N)]
STATE_MATRIX = [[-1] * N for size in range(N)]


#-1 is placeholder for missing transitions
TRANSITION_MATRIX = [
    [1, 2, -1, -1, -1, -1, -1], #for the stable/resting state (0)
    [1, 2, -1, -1, -1, -1, -1], #for the falling state (1),
    [-1, -1, 1, 1, 1, 3, -1], #for the pending state (2)
    [-1, -1, -1, -1, -1, -1, 0] #for the blocked state (3)
]
    
#CONDITIONS
# 0 - the cell below is empty/free
# 1 - the cell below is blocked/taken/confused
# 2 - the lower left cell is free
# 3 - the lower right cell is free
# 4 - both lower cells are free
# 5 - nowhere to go
# 6 - settling

def determine_condition(row: int, col: int):
    condition = -1
    if row + 1 < N: #check if naay valid nga lower cell
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
            if row + 1 < N and col - 1 >= 0: #check if naay valid nga lower left cell
                if GRID[row + 1][col - 1] == 0: #free si left cell
                    is_left_free = True

            if row + 1 < N and col + 1 < N: #check if naay valid nga lower right cell
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
        #if na reach na ang bottom, dili na mo move dapat
        #transition from falling - pending - blocked - resting
        
        # condition = 1
        # current_state = STATE_MATRIX[row][col]
        # STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to pending
         
        # condition = 5
        # current_state = STATE_MATRIX[row][col]
        # STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to blocked (nowhere to go)
        
        # condition = 6
        # current_state = STATE_MATRIX[row][col]
        # STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition] #transition to to resting
        
        #we can make this slighly elegant using a loop hahaha
        conditions = [1, 5, 6]
        for condition in conditions:
            current_state = STATE_MATRIX[row][col]
            STATE_MATRIX[row][col] = TRANSITION_MATRIX[current_state][condition]
    
def is_column_full(col: int):
    has_empty_cell = False
    for i in range(N):
        if GRID[i][col] == 0:
            has_empty_cell = True
    
    return not has_empty_cell
        
def is_sand_container_full():
    free_columns = 0
    for i in range(N):
        if not is_column_full(i):
            free_columns += 1
    
    return free_columns == 0

def copy_grid():
    for i in range(N):
        for j in range(N):
            GRID[i][j] = NEXT_GRID[i][j]

def print_grid():
    for i in range(N):
        line = ""
        for j in range(N):
            if GRID[i][j] == 0:
                line += " -"
            else:
                line += " *"
        print(line)
        
    print()

def main():        
    print("Sand Container Initialized")
    print_grid()
    
    is_running = True
    while is_running:
        print("Choose Next Course of Action")
        print("--- Add Sand - Press 1\n--- Render Next Grid State - Press Enter or Any Key\n--- Exit Program - Press 0")
        action = input("Action: ")
        
        if action == "0":
            is_running = False
            print("Simulation Terminated...")
            continue
        
        if action == "1":
            #ask for a valid input of column to add the sand
            valid_col = False
            col_to_drop = 0 #default to first column as placeholder value
            while not valid_col:
                try:
                    col_to_drop = int(input(f"Enter the column to drop the sand 0 - {N - 1}: "))
                except:
                    print("Invalid number, please try again.")
                    continue
                if col_to_drop < 0 or col_to_drop >= N:
                    print("Invalid column, please try again.")
                #TODO add a checker if napuno na ang column
                elif is_column_full(col_to_drop):
                    print("Column is already full, please try again.")
                else:
                    valid_col = True
            
            #at this point, naa natay valid nga column
            
            #i add na nato ang sand sa top sa column
            GRID[0][col_to_drop] = 1 
            # NEXT_GRID[0][col_to_drop] = 1
            #i add sad nato sha sa state matrix
            STATE_MATRIX[0][col_to_drop] = 0 #start staet is at rest
                        
        #mo loop nata sa every sand sa GRID, tas idetermine ang next_GRID        
        print("----- Current Sand Container -----")
        print_grid()
            
        for i in range(N - 1, -1, -1):
            for j in range(N):
                condition = -1 #placeholder value
                #TODO problematic ni sha if example ang sa new_grid kay ni adto nislide sa right
                #dayon karon kay sa loop sa grid kay empty man to pa so iyahang ipa fall ang sand
                #mag conflict na sila
                if GRID[i][j] != 0:
                    #now ilihok na nato ang grid, meaning pa move-on na nato ang mga sands
                    # with this, mausab sad ang state matrix, i follow ra nato ang location sa mga sands
                    condition = determine_condition(i, j)
                        
                    #diri na part, mag move nata sa mga sands
                    if condition == 0 and STATE_MATRIX[i][j] == 1: #falling, move sa below
                        state = STATE_MATRIX[i][j]
                        GRID[i][j] = 0 #the last location kay i empty na nato
                        GRID[i + 1][j] = 1 #balhin na sa new loc, which is down
                        STATE_MATRIX[i][j] = -1 #meaning ra ana wala ta ga keep track ana nga cell
                        STATE_MATRIX[i + 1][j] = state
                    elif condition == 2 and STATE_MATRIX[i][j] == 1: #meaning pending to falling, move left
                        state = STATE_MATRIX[i][j]
                        GRID[i][j] = 0
                        GRID[i + 1][j - 1] = 1
                        STATE_MATRIX[i][j] = -1
                        STATE_MATRIX[i + 1][j - 1] = state
                    elif condition == 3 and STATE_MATRIX[i][j] == 1: #meaning pending to falling, move right
                        state = STATE_MATRIX[i][j]
                        GRID[i][j] = 0
                        GRID[i + 1][j + 1] = 1
                        STATE_MATRIX[i][j] = -1
                        STATE_MATRIX[i + 1][j + 1] = state
                    elif condition == 4 and STATE_MATRIX[i][j] == 1: #meaning pending to falling, move left or right
                        state = STATE_MATRIX[i][j]
                        GRID[i][j] = 0
                        
                        #1 - left, 2 - right
                        random_number = random.randint(1, 2)
                        
                        if random_number == 1:
                            GRID[i + 1][j - 1] = 1
                            STATE_MATRIX[i][j] = -1
                            STATE_MATRIX[i + 1][j - 1] = state
                        elif random_number == 2:
                            GRID[i + 1][j + 1] = 1
                            STATE_MATRIX[i][j] = -1
                            STATE_MATRIX[i + 1][j + 1] = state  
                    elif condition == 5 and STATE_MATRIX[i][j] == 3: #blocked, transition to resting
                        condition = 6 #condition 6 is for settling to resting state
                        current_state = STATE_MATRIX[i][j]
                        STATE_MATRIX[i][j] = TRANSITION_MATRIX[current_state][condition] #nahimo na siya nga resting
                    
        print("----- Sand Container After Transition -----")
        # copy_grid()
        print_grid()
        
        if is_sand_container_full():
            is_running = False
            print("The sand container is full. Please reset the simulation...")
        


if __name__ == "__main__":
    main()