import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def initialize_grid(size, density):
    grid = np.random.choice([0, 1], size=(size, size), p=[1 - density, density])
    return grid

def update(frameNum, img, grid, size):
    newGrid = grid.copy()

    for i in range(size):
        for j in range(size):
            # Count the number of alive neighbors
            total = int((grid[i, (j-1)%size] + grid[i, (j+1)%size] +
                         grid[(i-1)%size, j] + grid[(i+1)%size, j] +
                         grid[(i-1)%size, (j-1)%size] + grid[(i-1)%size, (j+1)%size] +
                         grid[(i+1)%size, (j-1)%size] + grid[(i+1)%size, (j+1)%size])/255)

            # Apply the rules of the Game of Life
            if grid[i, j] == 1:  # Cell is alive (cloud particle)
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0  # Die (clear sky)
            else:  # Cell is dead (clear sky)
                if total == 3:
                    newGrid[i, j] = 1  # Reproduce (cloud particle)

    img.set_data(newGrid)
    grid[:] = newGrid
    return img

def main():
    # Parameters
    size = 50  # Size of the grid
    density = 0.3  # Initial density of cloud particles

    # Initialize grid
    grid = initialize_grid(size, density)

    # Set up the plot
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, size), frames=100, interval=100, save_count=50)

    plt.show()

if __name__ == "__main__":
    main()