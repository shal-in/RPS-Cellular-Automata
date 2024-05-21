import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
import os

# Code for simulation
def generate_grid(states=3, size=(10, 10)):
    return np.random.randint(0, states, size=size)

def tally_neighbourhood(cell, grid, states):
    cell_i, cell_j = cell
    min_i = max(0, cell_i - 1)
    min_j = max(0, cell_j - 1)
    max_i = min(cell_i + 1, grid.shape[0] - 1)
    max_j = min(cell_j + 1, grid.shape[1] - 1)

    neighbourhood = grid[min_i:max_i + 1, min_j:max_j + 1]
    state = grid[cell_i, cell_j]

    tally = {i: 0 for i in range(states)}
    tally[state] -= 1  # subtract the state of the current cell because it will be counted in the neighbourhood

    for value in neighbourhood.flatten():
        tally[value] += 1

    return tally

def calculate_new_state(state, tally, threshold, states):
    opponent = (state + 1) % states
    if tally[opponent] >= threshold:
        return opponent
    return state

def run_simulation(grid, states=3, threshold=2):
    new_grid = np.empty_like(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            tally = tally_neighbourhood((i, j), grid, states)
            new_state = calculate_new_state(grid[i, j], tally, threshold, states)
            new_grid[i, j] = new_state
    return new_grid












# Helper code for data processing, animations, etc
def generate_file(states, size, threshold, intervals, description=None):
    i = 0
    filename = f"states{states}-threshold{threshold}-intervals{intervals}"
    while os.path.exists(f"outputs/{filename}.txt"):
        i += 1
        filename = f"states{states}-threshold{threshold}-intervals{intervals}-({i})"

    with open(f"outputs/{filename}.txt", "w") as file:
        file.write(f">states={states},size={size},threshold={threshold},intervals={intervals},description={description}\n")

    return filename


def read_grids_from_file(filename):
    grids = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    current_grid = []
    for line in lines[1:]:  # Skip the first row (description)
        if '>' in line.strip():
            if current_grid:
                grids.append(np.array(current_grid, dtype=int))
                current_grid = []
        else:
            current_grid.append(list(map(int, line.strip().split())))

    # Append the last grid if it exists
    if current_grid:
        grids.append(np.array(current_grid, dtype=int))

    return grids


def create_animation_from_file(filename, fps=24, interval=75, show_animation=True, save_as_gif=False):
    # Read grids from file
    grids = read_grids_from_file(f"outputs/{filename}.txt")
    
    # Determine the aspect ratio of the grids (assuming they are square)
    grid_shape = grids[0].shape
    aspect_ratio = grid_shape[1] / grid_shape[0]
    
    # Define hex color values for custom colormap
    colors = ['#006C67', '#F194B4', '#003844', '#FFB100', '#FFEBC6', '#B3C0A4', '#6C91C2', '#DBD56E', '#7D7C84', '#DE1A1A']
    n_bins = [0.0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 1]  # Boundaries for the colors
    
    # Create colormap
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", list(zip(n_bins, colors)))
    
    # Create a figure and a set of subplots for the animation
    fig, ax = plt.subplots(figsize=(aspect_ratio * 5, 5))  # Adjust the figure size based on the aspect ratio
    cax = ax.matshow(grids[0], cmap=custom_cmap)
    
    # Remove axis labels and ticks
    ax.axis('off')
    
    def update(frame):
        cax.set_array(grids[frame])
        return [cax]
    
    # Create the animation using FuncAnimation
    ani = animation.FuncAnimation(fig, update, frames=len(grids), interval=interval, blit=True)
    
    # Remove margins and make the figure fill the screen
    fig.tight_layout(pad=0)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    if save_as_gif:
        # Save the animation as a GIF
        ani.save(f"outputs/{filename}.gif", writer='pillow', fps=fps)
    
    if show_animation:
        # Show the animation
        plt.show()

def get_current_time():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the date and time
    formatted_datetime = current_datetime.strftime("%H:%M:%S")

    return formatted_datetime