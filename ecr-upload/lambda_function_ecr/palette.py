from math import sqrt
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
import urllib.request
from PIL import Image
from io import BytesIO
from pprint import pprint
from utils import (
    plot_color_proportions,
    display_images_with_scores_and_colors,
)
from typing import Tuple
import numpy as np
from skimage.color import rgb2lab

DOMINANT_COLOR_CUTOFF = 12
COLLAGE_SIZE = 9
MAX_SIZE = 250
DARK_THRESHOLD = 130
LIGHT_THRESHOLD = 255 * 3 - DARK_THRESHOLD
CLOSENESS_CUTOFF = 35
COMPLEMENTARY_COLOR_WEIGHTAGE = 0.6


def get_complimentary_color(color):
    """
    Takes in color, a triplet of RGB values
    returns complimentary color
    """
    return tuple([255 - i for i in color])


# Function to convert RGB to LAB
def rgb_to_lab(rgb_color: Tuple[int, int, int]) -> np.ndarray:
    """
    Convert an RGB color to LAB color space.

    Parameters:
    rgb_color (Tuple[int, int, int]): The RGB color as a tuple (R, G, B).

    Returns:
    np.ndarray: The LAB color as an array.
    """
    # RGB values must be in the range [0, 1] for the conversion
    return rgb2lab(np.array([[rgb_color]]) / 255.0).flatten()


# Function to calculate Delta E
def color_closeness_distance(
    rgb_color1: Tuple[int, int, int], rgb_color2: Tuple[int, int, int]
) -> float:
    """
    Calculate the Delta E similarity score between two RGB colors.

    Parameters:
    rgb_color1 (Tuple[int, int, int]): The first RGB color as a tuple (R, G, B).
    rgb_color2 (Tuple[int, int, int]): The second RGB color as a tuple (R, G, B).

    Returns:
    float: The Delta E similarity score.
    """
    # Convert RGB colors to LAB
    lab_color1 = rgb_to_lab(rgb_color1)
    lab_color2 = rgb_to_lab(rgb_color2)

    # Calculate the Euclidean distance between the two LAB colors
    distance = np.sqrt(np.sum((lab_color1 - lab_color2) ** 2))
    return distance


class PaletteFilter:
    def __init__(
        self,
        collage_size=COLLAGE_SIZE,
        dominant_color_cutoff=DOMINANT_COLOR_CUTOFF,
        max_image_size=MAX_SIZE,
        dark_threshold=DARK_THRESHOLD,
        light_threshold=LIGHT_THRESHOLD,
        closeness_cutoff=CLOSENESS_CUTOFF,
        complementary_color_weightage=COMPLEMENTARY_COLOR_WEIGHTAGE,
        number_of_means=10,
        less_frequent_decay_factor=1.00,
        local=False,
    ):
        self.collage_size = collage_size
        self.dominant_color_cutoff = dominant_color_cutoff
        self.max_image_size = max_image_size
        self.dark_threshold = dark_threshold
        self.light_threshold = light_threshold
        self.closeness_cutoff = closeness_cutoff
        self.complementary_color_weightage = complementary_color_weightage
        self.number_of_means = number_of_means
        self.less_frequent_decay_factor = less_frequent_decay_factor
        self.local = local

    def get_palette(self, path):
        """
        path: filepath of image
        n: number of colors to be put into palette

        returns a tuple of:
        - the opened image bytes
        - a list of the proportions of each color in the image, as a tuple of
        (proportion, color)
        """
        if not self.local:
            with urllib.request.urlopen(path) as resp:
                image_data = resp.read()
            image_opened = Image.open(BytesIO(image_data))
        else:
            image_opened = Image.open(path)

        # Resize the image to speed up computation
        image_opened.thumbnail((self.max_image_size, self.max_image_size))
        img = np.array(image_opened.convert("RGB"))

        k_cluster = KMeans(n_clusters=self.number_of_means, n_init=10)
        k_cluster.fit(img.reshape(-1, 3))

        n_pixels = len(k_cluster.labels_)
        counter = Counter(
            k_cluster.labels_
        )  # count how many pixels per cluster
        perc = {}
        for i in counter:
            perc[i] = np.round(counter[i] / n_pixels, 2)
        perc = dict(sorted(perc.items()))

        proportion_to_color = [
            (
                perc[i],
                (
                    k_cluster.cluster_centers_[i][0],
                    k_cluster.cluster_centers_[i][1],
                    k_cluster.cluster_centers_[i][2],
                ),
            )
            for i in range(self.number_of_means)
        ]
        proportion_to_color.sort(key=lambda x: x[0], reverse=True)
        return (img, proportion_to_color)

    def get_predominant_colors(self, image_datas):
        """
        each image's colors is a ranked list of
        [[proportion1, RGB color1],
        [proportion2, RGB color2]...]

        upweights the color of more popular images

        returns the top k colors

        Takes a list of dominant colors and returns the top k overall dominant colors.
        Each entry in dominant_colors is expected to be a tuple (color, proportion),
        where color is an RGB tuple.
        """
        k = 5
        dominant_colors = [
            image_data["colors"] for image_data in image_datas
        ]
        # Flatten the list of dominant colors and create a weighted list
        weighted_colors = []
        for image_colors in dominant_colors:
            for i, (proportion, color) in enumerate(image_colors):
                # Repeat the color proportion*100 times
                weighted_colors.extend(
                    [
                        color
                        for _ in range(
                            int(
                                proportion
                                * 100
                                * (self.less_frequent_decay_factor**i)
                            )
                        )
                    ]
                )

        weighted_colors = np.array(weighted_colors)

        # Perform k-means clustering to find top k colors
        kmeans = KMeans(n_clusters=k)
        labels = kmeans.fit_predict(weighted_colors)

        # Count the labels to find the proportion of each cluster
        label_counts = np.bincount(labels)
        total_count = np.sum(label_counts)
        proportions = label_counts / total_count

        # The cluster centers are the top k dominant colors
        dominant_colors_with_proportions = [
            (
                proportion,
                tuple(map(int, center)),
            )
            for center, proportion in zip(
                kmeans.cluster_centers_, proportions
            )
        ]

        dominant_colors_with_proportions.sort(
            key=lambda x: x[0], reverse=True
        )

        return dominant_colors_with_proportions

    def is_too_dark_or_light(self, color):
        """
        Takes in a color, a triplet of RGB values
        returns true if the color is too dark
        """
        return (
            sum(color) < self.dark_threshold
            or sum(color) > self.light_threshold
        )

    def get_single_image_distance(self, image_colors, compare_color):
        """
        each image's colors is a ranked list of
        [[proportion1, RGB color1], [proportion2, RGB color2]...]

        RGB colors are tuplets of RGB values
        """
        total_score = 0
        for proportion, color in image_colors:
            closeness_score = color_closeness_distance(
                color, compare_color
            )
            total_score += proportion * closeness_score

        return total_score

    def add_score_for_complementary_streak(
        self, image_datas, complementary_color
    ):
        """
        each image's colors is a ranked list of
        [[proportion1, RGB color1], [proportion2, RGB color2]...]

        RGB colors are tuplets of RGB values
        """

        for image_data in image_datas:
            for proportion, color in image_data["colors"]:
                closeness_score = color_closeness_distance(
                    color, complementary_color
                )
                if closeness_score < self.closeness_cutoff:
                    image_data["score"] -= (
                        image_data["score"]
                        * proportion
                        * self.complementary_color_weightage
                    )

        return image_datas

    def filter_images(self, image_urls):
        """
        1. Get the predominant color of all the images
        2. Get its complimentary color
        3. Assign each image a score based on
        - Its original rank in the list (its popularity)
        - The distance between the predominant color and the image's predominant color
        - The distance between the complimentary color and the image's predominant color
        """
        image_datas = []
        for i, image_url in enumerate(image_urls):
            (_, proportion_to_colors) = self.get_palette(image_url)
            image_datas.append(
                {
                    "url": image_url,
                    "colors": proportion_to_colors,
                    "rank": i,
                }
            )

        # get the predominant color
        predominant_colors = self.get_predominant_colors(image_datas)
        print("predominant colors:", predominant_colors)

        predominant_color = None
        for color in predominant_colors:
            if not self.is_too_dark_or_light(color[1]):
                predominant_color = color[1]
                break

        if predominant_color is None:
            predominant_color = predominant_colors[0][1]

        # get the image score for each image, weighting the score by its rank
        for image_data in image_datas:
            image_data["score"] = self.get_single_image_distance(
                image_data["colors"], predominant_color
            ) * (self.less_frequent_decay_factor ** image_data["rank"])

        # sort by score and cut off by dominant color cutoff
        image_datas.sort(key=lambda x: x["score"])

        image_datas = image_datas[: self.dominant_color_cutoff]

        # # get the complimentary color
        complimentary_color = get_complimentary_color(predominant_color)

        print(
            "dominant and complementary:",
            predominant_color,
            complimentary_color,
        )

        # display_images_with_scores_and_colors(
        #     [
        #         (
        #             img["url"],
        #             img["score"],
        #         )
        #         for img in image_datas
        #     ],
        #     predominant_color,
        #     complimentary_color,
        # )

        self.add_score_for_complementary_streak(
            image_datas, complimentary_color
        )
        image_datas.sort(key=lambda x: x["score"])

        # display_images_with_scores_and_colors(
        #     [
        #         (
        #             img["url"],
        #             img["score"],
        #         )
        #         for img in image_datas
        #     ],
        #     predominant_color,
        #     complimentary_color,
        # )

        # # cut-off top k
        image_datas = image_datas[: self.collage_size]

        return image_datas, predominant_color, complimentary_color


if __name__ == "__main__":
    url = "https://hips.hearstapps.com/hmg-prod/images/cutest-dog-breed-bernese-64356a43dbcc5.jpg"
    import glob

    red_images = glob.glob("..\\tests\\red\\*")
    pprint(red_images)

    p = PaletteFilter(local=True)

    scores = p.filter_images(
        red_images,
    )
