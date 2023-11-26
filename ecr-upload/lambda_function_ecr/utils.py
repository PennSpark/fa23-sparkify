import matplotlib.pyplot as plt
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import re


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from urllib.request import urlopen
from io import BytesIO


# Function to plot colors with proportions
def plot_color_proportions(color_data):
    # Create a figure and a single subplot
    fig, ax = plt.subplots(figsize=(8, 2))
    # The starting point for the first color
    start = 0
    # Iterate over the color data
    for proportion, color in color_data:
        # Draw a rectangle with the corresponding color and proportion
        ax.add_patch(
            plt.Rectangle(
                (start, 0), proportion, 1, color=np.array(color) / 255.0
            )
        )
        # Place the text in the middle of the colored rectangle
        ax.text(
            start + proportion / 2,
            0.5,
            f"{proportion:.0%}",
            va="center",
            ha="center",
            fontsize=12,
        )
        # Update the start position for the next color
        start += proportion

    # Set the limits of the plot to the start and end of the rectangles
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    # Remove the y axis
    ax.get_yaxis().set_visible(False)
    # Set the x ticks to empty because we don't need them
    ax.set_xticks([])
    # Remove the spines of the plot
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.show()


def display_images_with_scores_and_colors(
    images_with_scores, dominant_color, complementary_color
):
    """
    Displays images with their scores and a bar of dominant and complementary colors.

    Parameters:
    - images_with_scores: List of tuples, each containing the path to the image (either a local path or a URL) and its score.
    - dominant_color: Tuple representing the RGB values for the dominant color.
    - complementary_color: Tuple representing the RGB values for the complementary color.
    """

    # Normalize the RGB values to the range 0 to 1 for matplotlib
    dominant_color_normalized = tuple([c / 255.0 for c in dominant_color])
    complementary_color_normalized = tuple(
        [c / 255.0 for c in complementary_color]
    )

    # Create a figure and axis for the color bars
    fig_color, ax_color = plt.subplots(figsize=(6, 2))

    # Display the dominant and complementary color bars
    ax_color.barh(1, width=1, color=dominant_color_normalized, height=1)
    ax_color.barh(
        0, width=1, color=complementary_color_normalized, height=1
    )
    ax_color.set_xlim(0, 1)
    ax_color.set_ylim(-1, 2)
    ax_color.set_yticks([])
    ax_color.set_xticks([])
    ax_color.axis("off")
    ax_color.text(
        0.5,
        1,
        "Dominant Color",
        ha="center",
        va="center",
        fontsize=12,
        color="white",
    )
    ax_color.text(
        0.5,
        0,
        "Complementary Color",
        ha="center",
        va="center",
        fontsize=12,
        color="white",
    )

    # Set up the plot for images and scores
    num_images = len(images_with_scores)
    fig_images, axs_images = plt.subplots(
        1, num_images, figsize=(5 * num_images, 10)
    )
    if num_images == 1:
        axs_images = [axs_images]

    # Loop over each image and its score and display them
    for ax, (image_path, score) in zip(axs_images, images_with_scores):
        # Here we use placeholder images since we can't load actual images
        # Create a placeholder image using the dominant color
        if image_path.startswith("http"):  # If the image is a URL
            with urlopen(image_path) as url:
                f = BytesIO(url.read())
                img = mpimg.imread(f, format="JPG")
        else:  # If the image is a local file path
            img = mpimg.imread(image_path)

        ax.imshow(img)
        ax.set_title("Score: {:.1f}".format(score), fontsize=12)
        ax.axis("off")  # Turn off axis

    plt.tight_layout()
    plt.show()


def get_cropped_name(image_path, base_folder):
    """
    Returns the path to the cropped image (may be a URL)
    """
    print(image_path)
    # Split the image path into its components
    path_parts = re.split(r"[\\\/]", image_path)
    print(path_parts)
    filename = path_parts[-1]
    filename_parts = filename.split(".")
    # Replace the file extension with 'png'
    if len(filename_parts) == 1:
        filename_parts = filename_parts + ["png"]
    else:
        filename_parts[-1] = "png"

    # Reassemble the path with the modified filename
    print(filename_parts)
    full_path = (
        base_folder + "/" + filename_parts[0] + "." + filename_parts[1]
    )

    return full_path


if __name__ == "__main__":
    pass