
import numpy as np
from Pylette import extract_colors
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches


"""Octree creation."""

octree = oct.Octree(max_depth=4)






# 1. Load the image (replace 'image.jpg' with your image path)
# You can use PIL to load the image if needed, but pylette can also take a path string
image_path = 'image.jpg'

# 2. Extract the color palette
# Use the extract_colors function, specifying the desired palette size (e.g., 5 colors)
# You can also specify the mode (KMeans or MedianCut) and colorspace (RGB, HSV, HLS)
palette = extract_colors(image=image_path, palette_size=5, mode='KMeans')

# 3. Access and display the extracted colors
print(f"Extracted {len(palette.colors)} colors:")
for color in palette.colors:
    print(f"  RGB: {color.rgb}, Hex: {color.hex}, Frequency: {color.freq:.2%}")

# 4. (Optional) Display the palette visually
# This requires matplotlib
def display_palette(palette):
    fig, ax = plt.subplots(1, 1, figsize=(10, 2))
    # Sort colors by frequency for a consistent display
    sorted_colors = sorted(palette.colors, key=lambda c: c.freq, reverse=True)
    
    for i, color in enumerate(sorted_colors):
        # Create a rectangle for each color
        rect = patches.Rectangle((i / len(sorted_colors), 0), 1 / len(sorted_colors), 1, color=color.hex)
        ax.add_patch(rect)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Extracted Color Palette")
    plt.show()

# Uncomment the line below to display the palette
# display_palette(palette)


