import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import rps

filename = "output-0.txt"  # Change to your actual filename
grids = rps.read_grids_from_file(filename)

# Determine the aspect ratio of the grids (assuming they are square)
grid_shape = grids[0].shape
aspect_ratio = grid_shape[1] / grid_shape[0]

# Define hex color values for custom colormap
colors = ['#0A122A', '#698F3F', '#FBFAF8', '#804E49']
n_bins = [0.0, 0.33, 0.66, 1.0]  # Boundaries for the colors

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
ani = animation.FuncAnimation(fig, update, frames=len(grids), interval=75, blit=True)

# Remove margins and make the figure fill the screen
fig.tight_layout(pad=0)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Save the animation as a GIF
ani.save("simulation.gif", writer='pillow', fps=30)

# Show the animation
plt.show()