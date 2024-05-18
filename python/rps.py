import numpy as np

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
