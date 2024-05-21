import numpy as np
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
    filename = f"output-{i}.txt"
    while os.path.exists(filename):
        i += 1
        filename = f"output-{i}.txt"

    with open(filename, "w") as file:
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