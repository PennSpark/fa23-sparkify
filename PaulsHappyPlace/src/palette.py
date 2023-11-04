import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import Counter
import urllib.request
from PIL import Image
from io import BytesIO
from pprint import pprint


DOMINANT_COLOR_CUTOFF = 20
COLLAGE_SIZE = 10
IS_LOCAL = True


def get_palette(path, n, local=False):
    """
    path: filepath of image
    n: number of colors to be put into palette

    returns a tuple of:
    - the opened image bytes
    - a list of the proportions of each color in the image, as a tuple of
    (proportion, color)
    """
    if not local:
        with urllib.request.urlopen(path) as resp:
            image_data = resp.read()

        # Convert the image data to a PIL image
        image_opened = Image.open(BytesIO(image_data))
        img = np.array(image_opened)

    else:
        img = cv.cvtColor(cv.imread(path), cv.COLOR_BGR2RGB)

    k_cluster = KMeans(n_clusters=n, n_init=10)
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
        for i in range(n)
    ]
    proportion_to_color.sort(key=lambda x: x[0], reverse=True)
    return (img, proportion_to_color)


def show_imgs(img_1, img_2):
    f, ax = plt.subplots(1, 2, figsize=(10, 10))
    ax[0].imshow(img_1)
    ax[1].imshow(img_2)
    ax[0].axis("off")  # hide the axis
    ax[1].axis("off")
    f.tight_layout()
    plt.show()


def get_complimentary_color(color):
    """
    Takes in color, a triplet of RGB values
    returns complimentary color
    """
    return tuple([255 - i for i in color])


def color_closeness_score(color1, color2):
    """
    Takes in two triplets of RGB values
    returns a gaussian score based on the distance between them
    """
    distance = sum([(color1[i] - color2[i]) ** 2 for i in range(3)])
    bell_width = 1000
    return np.exp(-distance / bell_width).item()


def get_predominant_color(image_datas, decay_factor=0.95):
    """
    Takes in a list of triplets of RGB values
    returns the most common color

    each image's colors is a ranked list of
    [[proportion1, RGB color1], [proportion2, RGB color2]...]

    RGB colors are tuplets of RGB values

    upweights the color of more popular images
    (ie images that are higher up in the list)

    returns the top color

    TODO: Think about clustering colors among all the images
    because colors are not neccessarily EXACTLY the same
    """
    color_count = {}
    for image_data in image_datas:
        decay_i = decay_factor ** image_data["rank"]
        for proportion, color in image_data["colors"]:
            if color in color_count:
                color_count[color] += proportion * decay_i
            else:
                color_count[color] = proportion * decay_i

    return max(color_count, key=color_count.get)


def get_single_image_score(image_colors, compare_color):
    """
    each image's colors is a ranked list of
    [[proportion1, RGB color1], [proportion2, RGB color2]...]

    RGB colors are tuplets of RGB values
    """
    total_score = 0
    for image_color in image_colors:
        proportion = image_color[0]
        color = image_color[1]
        dominant_distance = color_closeness_score(color, compare_color)
        total_score += proportion * dominant_distance
    return total_score


def filter_images(image_urls, decay_factor=0.98):
    """
    1. Get the predominant color of all the images
    2. Get its complimentary color
    3. Assign each image a score based on
    - Its original rank in the list (its popularity)
    - The distance between the predominant color and the image's predominant color
    - The distance between the complimentary color and the image's predominant color
    """
    # TODO: get the color of each image in parallel
    image_datas = []
    for i, image_url in enumerate(image_urls):
        (_, proportion_to_colors) = get_palette(image_url, 5)
        image_datas.append(
            {"url": image_url, "colors": proportion_to_colors, "rank": i}
        )

    # get the predominant color
    predominant_color = get_predominant_color(image_datas)

    # get the image score for each image, weighting the score by its rank
    for image_data in image_datas:
        image_data["score"] = get_single_image_score(
            image_data["colors"], predominant_color
        ) * (decay_factor ** image_data["rank"])

    # sort by score and cut off by dominant color cutoff
    image_datas.sort(key=lambda x: x["score"])
    image_datas = image_datas[:DOMINANT_COLOR_CUTOFF]

    # get the complimentary color
    complimentary_color = get_complimentary_color(predominant_color)

    for image_data in image_datas:
        image_data["score"] += get_single_image_score(
            image_data["colors"], complimentary_color
        ) * (decay_factor ** image_data["rank"])

    # sort by score
    image_datas.sort(key=lambda x: x["score"])

    # cut-off top k
    image_datas = image_datas[:COLLAGE_SIZE]

    return image_datas


if __name__ == "__main__":
    url = "https://hips.hearstapps.com/hmg-prod/images/cutest-dog-breed-bernese-64356a43dbcc5.jpg"
    # (img, proportion_to_colors) = get_palette(
    #     "https://hips.hearstapps.com/hmg-prod/images/cutest-dog-breed-bernese-64356a43dbcc5.jpg",
    #     5,
    # )

    # # prints out RGB color codes and proportion of each color on image
    # for proportion_to_color in proportion_to_colors:
    #     proportion = proportion_to_color[0]
    #     color = proportion_to_color[1]
    #     print(
    #         f"Proportion: {proportion} Color: RGB({color[0]}, {color[1]}, {color[2]})"
    #     )

    # # showing image + palette for testing purposes
    # width = 300
    # palette = np.zeros((50, width, 3), np.uint8)

    # step = 0
    # for idx, proportion_to_color in enumerate(proportion_to_colors):
    #     color = proportion_to_color[1]
    #     proportion = proportion_to_color[0]
    #     palette[:, step : int(step + proportion * width + 1), :] = color
    #     step += int(proportion * width + 1)

    scores = filter_images(
        [
            "https://hips.hearstapps.com/hmg-prod/images/cutest-dog-breed-bernese-64356a43dbcc5.jpg",
        ]
    )
    pprint(scores)

    # show_imgs(img, palette)
