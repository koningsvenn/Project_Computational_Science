import numpy as np 
import numpy.random as random
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap


"""still decide on humidity levels and appropriate drop sizes"""
def initialize_grid(height, width, fall_heigth, humidity):
    """create a height x width grid with zeros representing empty cells or integers 
    to represent droplet size"""
    #empty grid
    grid = np.zeros((height + fall_heigth, width))
    #add droplets according to the relative humidity
    drops_amount = height * width * humidity
    
    #select random coordinates for each drop
    drops = 0
    while drops < drops_amount:
        n = random.randint(0, width)
        #no drops in the lower rows for falling space
        m = random.randint(0, height)
        #add the drop if the space is unoccupied
        if grid[m, n] == 0:
            #add a droplet of some size to the grid
            grid[m, n] = random.randint(1,5)
            #count one drop
            drops += 1
        
    return grid 

def wind(height, width, fall_heigth,wind_direction):
    """initialize a grid with wind directions, directions: up, down, left, right"""
    #empty grid
    wind = np.zeros((height + fall_heigth, width), dtype='<U5')
    #fill with the chosen direction and add some variation for random effects
    for m in range(height):
        for n in range(width):
            wind[m,n] = wind_direction
    
    return wind

def time_step_wind(grid, wind, rain_count, fall_heigth):
    """Perform a time step where the values move based on wind direction and merge."""
    height, width = grid.shape
    new_grid = np.zeros_like(grid)  # Initialize a new grid for the updated state
    #drop size that will cause it to become rain
    max_size = 10

    # Loop over all cells
    for m in range(height):
        for n in range(width):
            # If there is a non-zero value
            if grid[m, n] != 0:
                #check the drop size
                if grid[m, n] < max_size:
                    m_new, n_new = move(m, n)
                    # move and merge in the new grid
                    new_grid[m_new, n_new] += grid[m, n]
                else:
                    #drop becomes rain and it starts to fall
                    if m == height - 1:
                        #reached the bottom: remove and count rain
                        rain_count += 1
                    else:
                        n_new = n
                        m_new = m + 1
                        # move and merge in the new grid
                        new_grid[m_new, n_new] += grid[m, n]
            
            #add new small drops 
            probablility_new_drop = 0.0008   
            #if the position is empty and inside the cloud area
            if grid[m, n] == 0 and m < height - fall_heigth:
                if random.rand() < probablility_new_drop:
                    new_grid[m, n] = 1
            
            #split big drops
            probability_split_drop = 0.01
            #if the drop is large and inside the cloud area
            if grid[m, n] > 10 and m < height - fall_heigth:
                if random.rand() < probability_split_drop:
                    new_grid[m, n] = 1/2*grid[m, n]
                    if n == 0:
                        new_grid[m, n+1] = grid[m, n+1]+ 1/2*grid[m, n]
                    else:
                        new_grid[m, n-1] = grid[m, n-1]+ 1/2*grid[m, n]
                    print(m, n)

    return new_grid, rain_count

def move(m, n):
    """move the drops according to wind and random movements"""
    #chance of random movement
    p = 0.5
    #direction options
    directions = ['up', 'down', 'left', 'right']
    
    #get the wind direction from the wind grid(von Neumann neighborhood r=1)
    direction = wind[m, n]
    #the drop will move randomly with some chance p
    if random.uniform() < p:
        direction = random.choice(directions)

    # calculate new coordinates based on direction
    # using % operator to keep it within the system
    if direction == 'up':
        #boundary
        if m == 0:
            m_new = m + 1
        else:
            m_new = m - 1
        n_new = n
    elif direction == 'down':
        #boundary
        if  m == height - 1:
            m_new = m - 1
        else:
            m_new = (m + 1)
        n_new = n
    elif direction == 'left':
        #boundary
        if n == 0:
            n_new = n + 1
        else:
            n_new = n - 1
        m_new = m
    else:  # direction == 'right'
        #boundary
        if n == width - 1:
            n_new = n - 1
        else:
            n_new = n + 1
    m_new = m

    return m_new, n_new

    return new_grid

def time_step(grid):
    """Perform a time step where the values move in a random direction and merge."""
    height, width = grid.shape
    new_grid = np.zeros_like(grid)  # Initialize a new grid for the updated state

    # Loop over all cells
    for m in range(height):
        for n in range(width):
            # If there is a non-zero value
            if grid[m, n] != 0:
                # Pick a random direction (von Neumann neighborhood r=1)
                direction = random.choice(['up', 'down', 'left', 'right'])

                # calculate new coordinates based on direction
                # using % operator to keep it within the system
                if direction == 'up':
                    m_new = (m - 1) % height
                    n_new = n
                elif direction == 'down':
                    m_new = (m + 1) % height
                    n_new = n
                elif direction == 'left':
                    m_new = m
                    n_new = (n - 1) % width
                else:  # direction == 'right'
                    m_new = m
                    n_new = (n + 1) % width

                # move and merge in the new grid
                new_grid[m_new, n_new] += grid[m, n]
                
            #add new small drops 
            probablility_new_drop = 0.0008   
            if grid[m, n] == 0:
                if random.rand() < probablility_new_drop:
                    new_grid[m, n] = 1
            
            #split big drops
            probability_split_drop = 0.01
            if grid[m, n] > 10:
                if random.rand() < probability_split_drop:
                    new_grid[m, n] = 1/2*grid[m, n]
                    if n == 0:
                        new_grid[m, n+1] = grid[m, n+1]+ 1/2*grid[m, n]
                    else:
                        new_grid[m, n-1] = grid[m, n-1]+ 1/2*grid[m, n]
                    print(m, n)

    return new_grid


"""animation and plotting"""
def get_shades_of_blue(n):
    """Generate n shades of blue."""
    start = np.array([173, 216, 230]) / 255  # lightblue
    end = np.array([25, 25, 112]) / 255  # midnightblue
    return [(start + (end - start) * i / (n - 1)).tolist() for i in range(n)]

def animate_CA(initial_grid, wind, steps, interval, fall_heigth):
    """Animate the cellular automata, updating time step and cell values."""
    
    colors = get_shades_of_blue(20) 
    cmap = LinearSegmentedColormap.from_list("custom_blue", colors, N=256)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xticks(np.arange(-.5, initial_grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, initial_grid.shape[0], 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])

    grid = np.copy(initial_grid)
    matrix = ax.matshow(grid, cmap=cmap)

    # Create text objects for each cell
    text = [[ax.text(j, i, '', ha='center', va='center', color='black') for j in range(grid.shape[1])] for i in range(grid.shape[0])]

    #counter for rain
    rain_count = 0
    
    averages = []
    def update(frames):
        nonlocal grid
        nonlocal rain_count

        grid, rain_count = time_step_wind(grid, wind, fall_heigth, rain_count)  
        matrix.set_array(grid)
        print(rain_count)
        # Update text for each cell
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                val = grid[i, j]
                text_color = 'white' if val > 2 else 'black'  # Make values of dropletsize white or black for contrast
                text[i][j].set_text(f'{int(val)}' if val else '')
                text[i][j].set_color(text_color)
                text[i][j].set_visible(bool(val))  # Show text only for non-zero values

        #average dropsize
        non_zero_elements = np.count_nonzero(grid)
        average_size = np.sum(grid) / non_zero_elements if non_zero_elements else 0
        averages.append(int(average_size))

        ax.set_title(f"Animated cloud")
        return [matrix] + [txt for row in text for txt in row]

    ani = FuncAnimation(fig, update, frames=steps-1, interval=interval, blit=False, repeat=False) #Average step -1 because the first frame is a step and thus average dropletsize
    plt.show()
    return averages


def plot_averages(averages, steps):
    """Plot the average size of grid values over a given number of steps."""

    plt.figure(figsize=(10, 6))
    plt.plot(range(steps), averages, marker='o', linestyle='-', color='b')
    plt.title("Average Size of Droplets Over Time")
    plt.xlabel("Step")
    plt.ylabel("Average Size")
    plt.grid(True)
    plt.xticks(range(0, steps, max(1, steps // 10)))  
    plt.show()


height = 8
width = 10
fall_heigth = 1

grid = initialize_grid(height, width, fall_heigth, 0.5)
wind = wind(height, width, fall_heigth, 'left')
steps = 15
interval = 1000
averages = animate_CA(grid,wind,steps,interval,fall_heigth)
plot_averages(averages, steps)

