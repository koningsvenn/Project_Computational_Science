import numpy as np 
import numpy.random as random
import matplotlib.pyplot as plt 

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
    """perform a time step where the drops move in a random direction and merge"""
    new_grid = np.copy(grid)

    #loop over all cells
    height, width = grid.shape
    for m in range(height):
        for n in range(width):
            #if there is a drop
            if grid[m, n] != 0:
                #pick a random direction (von neuman neighborhood r=1)
                direction = random.randint(0, 4)
                """I don't know about this construction, there is probably a better way to do this"""
                #move up
                if direction == 0:
                    n_new = n
                    #periodic boundaries
                    if m == 0:
                        m_new = height - 1
                    else:
                        m_new = m - 1
                #move down
                elif direction == 1:
                    n_new = n
                    #periodic boundaries
                    if m == height - 1:
                        m_new = 0
                    else:
                        m_new = m + 1
                #move left
                elif direction == 2:
                    m_new = m
                    #periodic boundaries
                    if n == 0:
                        n_new = width - 1
                    else:
                        n_new = n - 1
                #move right
                else:
                    m_new = m
                    #periodic boundaries
                    if n == width - 1:
                        n_new = 0
                    else:
                        n_new = n + 1
                
                #write into new grid
                new_grid[m_new, n_new] += grid[m, n]
    return new_grid


    


grid = initialize_grid(5, 6, 0.5)
print(grid)
new_grid = time_step(grid)
print(new_grid)



