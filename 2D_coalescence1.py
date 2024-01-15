import numpy as np 
import numpy.random as random
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap


"""still decide on humidity levels and appropriate drop sizes"""
def initialize_grid(height, width, humidity):
    """create a height x width grid with zeros representing empty cells or integers 
    to represent droplet size"""
    #empty grid
    grid = np.zeros((height, width))
    #add droplets according to the relative humidity
    drops_amount = height * width * humidity
    #select random coordinates for each drop
    drops = 0
    while drops < drops_amount:
        n = random.randint(0, width)
        m = random.randint(0, height)
        #add the drop if the space is unoccupied
        if grid[m, n] == 0:
            #add a droplet of some size to the grid
            grid[m, n] = random.randint(1,5)
            #count one drop
            drops += 1
        
    return grid 

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

    return new_grid


def get_shades_of_blue(n):
    """Generate n shades of blue."""
    start = np.array([173, 216, 230]) / 255  # lightblue
    end = np.array([25, 25, 112]) / 255  # midnightblue
    return [(start + (end - start) * i / (n - 1)).tolist() for i in range(n)]


def animate_CA(initial_grid, steps=10, interval=2000):
    """Animate the cellular automata, updating time step and cell values."""

    # generate 15 shades of blue to show droplet size, want maybe numbers instead...
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

    # gunction to update the plot
    def update(frames):
        nonlocal grid
        grid = time_step(grid)
        matrix.set_array(grid)

        # clear previous text (values)
        [t.remove() for t in ax.texts]
        # add new text (values) for each cell
        for (i, j), val in np.ndenumerate(grid):
            if val:  # only show non-zero values
                text_color = 'black' if val < 3 else 'white'  # doesnt work yet, it updates text values each update but somehow doesnt show 
                ax.text(j, i, int(val), ha='center', va='center', color=text_color)

        ax.set_title(f"Time Step: {frames + 1}")
        return [matrix]

    ani = FuncAnimation(fig, update, frames=steps, interval=interval, blit=True, repeat=False)
    plt.show()


    
grid = initialize_grid(5, 6, 0.5)
steps = 10
interval = 1000
animate_CA(grid,steps,interval)

# print(grid)
# new_grid = time_step(grid)
# print(new_grid)




