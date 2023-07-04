import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set the grid size and number of time steps
grid_size = 50
num_steps = 100

# Set the initial parameters
initial_infected = 5
infection_rate = 0.3
recovery_rate = 0.1

# Initialize the grid
grid = np.zeros((grid_size, grid_size))

# Randomly infect a few cells
infected_indices = np.random.choice(range(grid_size**2), size=initial_infected, replace=False)
grid[np.unravel_index(infected_indices, (grid_size, grid_size))] = 1

# Initialize the figure and axis
fig, ax = plt.subplots()

# Function to update the grid at each time step
def update(step):
    global grid

    # Compute the number of infected neighbors for each cell
    num_infected_neighbors = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 1:  # Infectious cell
                # Check the neighboring cells
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < grid_size and 0 <= nj < grid_size:
                        if grid[ni, nj] == 0:  # Susceptible cell
                            num_infected_neighbors[ni, nj] += 1

    # Update the grid based on the SIR model
    new_grid = np.copy(grid)
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i, j] == 0:  # Susceptible cell
                if np.random.random() < infection_rate * num_infected_neighbors[i, j]:
                    new_grid[i, j] = 1  # Infect the cell
            elif grid[i, j] == 1:  # Infectious cell
                if np.random.random() < recovery_rate:
                    new_grid[i, j] = 2  # Recover the cell


    # Update the grid
    grid = new_grid

    # Clear the previous plot
    ax.clear()

    # Plot the grid
    ax.imshow(grid, cmap='RdYlBu', vmin=0, vmax=2, aspect='equal')

    # Set plot title and labels
    ax.set_title(f"Step: {step+1}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

# Create the animation
ani = FuncAnimation(fig, update, frames=num_steps, interval=200)

# Show the animation
plt.show()
