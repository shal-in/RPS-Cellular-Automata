import rps

# Example usage:
for i in range(16,18):
    filename = f"output-{i}"  # Change to your actual filename
    rps.create_animation_from_file(filename, show_animation=False, save_as_gif=True)

    print (f"{filename}.gif saved.")