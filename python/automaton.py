import rps

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

states = 3
size = (100, 100)
threshold = 4

grid = rps.generate_grid(states, size=size)

grids = [grid]

i = 0
while i < 1000:
    grid = rps.run_simulation(grid, states, threshold)
    grids.append(grid.copy())  # Ensure to append a copy of the grid to avoid reference issues
    i += 1

    if i % 50 == 0:
        print (i)

# Create a figure and a set of subplots
fig, ax = plt.subplots()
cax = ax.matshow(grids[0], cmap="viridis")
fig.colorbar(cax)  # Add a color bar for reference

def update(frame):
    cax.set_array(grids[frame])

ani = animation.FuncAnimation(fig, update, frames=len(grids), interval=100)

plt.show()
