import matplotlib.pyplot as plt 


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
