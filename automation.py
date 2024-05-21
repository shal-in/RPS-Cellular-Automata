import rps
import numpy as np

with open("automation.txt", "r") as file:
    lines = file.readlines()

for line in lines[1:]:
        # Split the line by commas
    parameters = line.strip().split(",")

    # Extract the individual parameters
    states = int(parameters[0])
    size_str = parameters[1].strip("()")
    size_values = size_str.split("x")
    size = tuple(map(int, size_values))
    threshold = int(parameters[2])
    intervals = int(parameters[3])
    description = parameters[4]

    filename = rps.generate_file(states, size, threshold, intervals, description)

    grid = rps.generate_grid(states, size=size)

    print (f"Starting simulation of {filename}; {rps.get_current_time()}")
    i=0
    while i < intervals:
        grid = rps.run_simulation(grid, states, threshold)

        with open(f"outputs/{filename}.txt", "a") as file:
            file.write(f"> {i}\n")
            np.savetxt(file, grid, fmt="%d")

        if i % 5 == 0:
            print (f"Progress: {i}/{intervals} at {rps.get_current_time()}")
        
        i += 1

    print (f"Data saved to {filename}.txt")
    
    with open("file-tracker.txt", "a") as file_tracker:
        file_tracker.write(f"\n{filename}.txt - states:{states}, size:{size}, threshold:{threshold}, intervals:{intervals}, description:{description}, comments: ")

    rps.create_animation_from_file(filename, show_animation=False, save_as_gif=True)