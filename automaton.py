import rps
import numpy as np

states = 3
size = (250, 250)
threshold = 3
intervals = 250
description = None

filename = rps.generate_file(states, size, threshold, intervals, description)

grid = rps.generate_grid(states, size=size)

# grids = [grid]

print ("Starting simulation. Standby...")
i = 0
while i < intervals:
    grid = rps.run_simulation(grid, states, threshold)
    # grids.append(grid.copy())  # Ensure to append a copy of the grid to avoid reference issues

    with open(filename, "a") as file:
        file.write(f">{i}\n")
        np.savetxt(file, grid, fmt="%d")

    i += 1
    if i % 20 == 0:
        print (i)


print (f"Data saved to {filename}")
