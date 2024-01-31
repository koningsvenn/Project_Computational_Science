import numpy as np 
import numpy.random as random
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import datetime
import os

"""set up the"""
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

def initialize_wind(height, width, fall_heigth,wind_direction):
    """initialize a grid with wind directions, directions: up, down, left, right"""
    #empty grid
    wind = np.zeros((height + fall_heigth, width), dtype='<U5')
    #fill with the chosen direction and add some variation for random effects
    for m in range(height):
        for n in range(width):
            wind[m,n] = wind_direction
    
    return wind

"""Time steps and movement"""

def time_step_wind(grid, wind, fall_heigth,probablility_new_drop,probability_split_drop):
    """Perform a time step where the values move based on wind direction and merge."""
    height, width = grid.shape
    new_grid = np.zeros_like(grid)  # Initialize a new grid for the updated state
    #drop size that will cause it to become rain
    max_size = 10

    # data that gets returned
    total_drops = 0
    max_drop_size = 0
    rain_count = 0

    # Loop over all cells
    for m in range(height):
        for n in range(width):
            if grid[m, n] > 0:
                total_drops += 1
                max_drop_size = int(max(max_drop_size, grid[m, n]))

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
            

            #if the position is empty and inside the cloud area
            if grid[m, n] == 0 and m < height - fall_heigth:
                if random.rand() < probablility_new_drop:
                    new_grid[m, n] = 1
            

            #if the drop is large and inside the cloud area
            if grid[m, n] > 10 and m < height - fall_heigth:
                if random.rand() < probability_split_drop:
                    new_grid[m, n] = 1/2*grid[m, n]
                    if n == 0:
                        new_grid[m, n+1] = grid[m, n+1]+ 1/2*grid[m, n]
                    else:
                        new_grid[m, n-1] = grid[m, n-1]+ 1/2*grid[m, n]
                    #print(m, n)
    
    return new_grid, rain_count, total_drops, max_drop_size

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
       #periodic boundary
        n_new = (n - 1) % width
        m_new = m
    else:  # direction == 'right'
        #periodic boundary
        n_new = (n + 1) % width
    m_new = m

    return m_new, n_new

    return new_grid

"""animation and plotting"""

def get_shades_of_blue(n):
    """Generate n shades of blue."""
    start = np.array([173, 216, 230]) / 255  # lightblue
    end = np.array([25, 25, 112]) / 255  # midnightblue
    return [(start + (end - start) * i / (n - 1)).tolist() for i in range(n)]

def animate_CA(initial_grid, wind, steps, interval, fall_heigth,probablility_new_drop,probability_split_drop):
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

    #lists to collect data
    averages = []
    raind_count_list = []
    total_drops_list = []
    max_drop_size_list = []
    def update(frames):
        nonlocal grid

        grid, rain_count,total_drops,max_drop_size = time_step_wind(grid, wind,fall_heigth, probablility_new_drop,probability_split_drop)  
        matrix.set_array(grid)
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
        raind_count_list.append(rain_count)
        total_drops_list.append(total_drops)
        max_drop_size_list.append(max_drop_size)

        ax.set_title(f"Animated cloud")
        return [matrix] + [txt for row in text for txt in row]

    ani = FuncAnimation(fig, update, frames=steps-1, interval=interval, blit=False, repeat=False) #Average step -1 because the first frame is a step and thus average dropletsize
    plt.show()
    return averages, raind_count_list,total_drops_list,max_drop_size_list

def plot_humidities(humidities, y, y_std,axis_name, unit):
    """plot the outcomes of the simulation against the humidities"""
    plt.figure()
    plt.errorbar(humidities, y, yerr=y_std, ecolor='orange')
    plt.xlabel('relative humidity')
    plt.ylabel(f'average {axis_name} [{unit}]')
    plt.savefig(f'figures/{axis_name}_humidity')

"""run experiments and collect data"""

def run_simulation(initial_grid, wind, steps, fall_heigth,probablility_new_drop,probability_split_drop):
    """run a cloud simulation without animation"""
    #set up the grid
    grid = np.copy(initial_grid)

    #lists to collect data
    averages = []
    raind_count_list = []
    total_drops_list = []
    max_drop_size_list = []

    #run steps amount of time steps
    for i in range(steps):
        grid, rain_count,total_drops,max_drop_size = time_step_wind(grid, wind,fall_heigth, probablility_new_drop,probability_split_drop)
        #average dropsize
        non_zero_elements = np.count_nonzero(grid)
        average_size = np.sum(grid) / non_zero_elements if non_zero_elements else 0
        #add data to lists
        averages.append(int(average_size))
        raind_count_list.append(rain_count)
        total_drops_list.append(total_drops)
        max_drop_size_list.append(max_drop_size)
    
    return averages, raind_count_list,total_drops_list,max_drop_size_list


def collect_data(data):
    df = pd.DataFrame(data)
    # Get current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Parameters for filename 
    param_str = f"fh{fall_heigth}_pnd{probablility_new_drop}_psd{probability_split_drop}"

    # Create filename and export
    filename = f"./exported_data/{current_datetime}_{param_str}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)

def run_experiment(height,width,humidity,wind_direction,steps,fall_heigth,probablility_new_drop,probability_split_drop):
    """run a few simulations and take the averages"""
    grid = initialize_grid(height, width, fall_heigth, humidity)
    wind = initialize_wind(height, width, fall_heigth, wind_direction)

    rain_mean_list = []
    size_mean_list = []
    total_mean_list = []
    max_drop_mean_list = []

    n = 40
    for i in range(n):
        averages,rain_count_list,total_drops_list,max_drop_size_list = run_simulation(grid,wind,steps,fall_heigth,probablility_new_drop,probability_split_drop)
        rain_mean_list.append(np.mean(rain_count_list))
        size_mean_list.append(np.mean(averages))
        total_mean_list.append(np.mean(total_drops_list))
        max_drop_mean_list.append(np.mean(max_drop_size_list))

    rain_mean = np.mean(rain_mean_list)
    rain_std = np.std(rain_mean_list)
    size_mean = np.mean(size_mean_list)
    size_std = np.std(size_mean_list)
    total_mean = np.mean(total_mean_list)
    total_std = np.std(total_mean_list)
    max_drop_mean = np.mean(max_drop_mean_list)
    max_drop_std = np.std(max_drop_mean_list)
    
    return rain_mean, rain_std, size_mean, size_std, total_mean, total_std, max_drop_mean, max_drop_std


"""input parameters"""
height = 50
width = 50
fall_heigth = 1
probablility_new_drop = 0.0008   
probability_split_drop = 0.01
steps = 1000
interval = 100
humidity = 0.5
wind_direction = 'left'

"""set up grid and wind"""
grid = initialize_grid(height, width, fall_heigth, humidity)
wind = initialize_wind(height, width, fall_heigth, wind_direction)

"""animation"""
# averages,rain_count_list,total_drops_list,max_drop_size_list = animate_CA(grid,wind,steps,interval,fall_heigth,probablility_new_drop,probability_split_drop)
# data = {
#     'Time_step': range(steps),
#     'Average droplet size': averages,
#     'Rain Count': rain_count_list,
#     'Total Drops': total_drops_list,
#     'Max Drop Size': max_drop_size_list
#     }
# collect_data(data)

"""simulate"""
#humidity range
humidities = np.arange(0.05, 1, 0.1)
#lists to store outcomes
rain_means = []
rain_stds = []
size_means = []
size_stds = []
total_means = []
total_stds = []
max_drop_means = []
max_drop_stds = []

#simulate for each
for i, humidity in enumerate(humidities):
    #updates
    print(f'{i+1}/{len(humidities)}: humidity = {humidity:.2f}')
    rain_mean, rain_std, size_mean, size_std, total_mean, total_std, max_drop_mean, max_drop_std = run_experiment(height, width, humidity, wind_direction, steps, fall_heigth, probablility_new_drop, probability_split_drop)
    #add data to lists
    rain_means.append(rain_mean)
    rain_stds.append(rain_std)
    size_means.append(size_mean)
    size_stds.append(size_std)
    total_means.append(total_mean)
    total_stds.append(total_std)
    max_drop_means.append(max_drop_mean)
    max_drop_stds.append(max_drop_std)

#collect and save data
data = {
    'Humidities': humidities,
    'Rain_mean': rain_means,
    'Rain_std': rain_stds,
    'Size_mean': size_means,
    'Size_std': size_stds,
    'Total_drops_mean': total_means,
    'Total_drops_std': total_stds,
    'Max_drop_mean': max_drop_means,
    'Max_drop_std': max_drop_stds
    }
collect_data(data)

#plot
plot_humidities(humidities, rain_means, rain_stds, 'rainfall', 'drops/time-step')
plot_humidities(humidities, size_means, size_stds, 'drop size', '/time-step')
plot_humidities(humidities, total_means, total_stds, 'total drops', '/time-step')
plot_humidities(humidities, max_drop_means, max_drop_stds, 'max drop size', '/time-step')

