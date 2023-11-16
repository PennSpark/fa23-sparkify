import json
from palette import PaletteFilter
from extractor import extract_objects_from_image, save_image_png
import random
import glob
from pprint import pprint
from utils import get_cropped_name

PERCENT_CROPPED = 0.6
LOCAL_BASE_FOLDER = "..\\tests\\red-extract"
# TODO: Add S3_BASE_FOLDER
S3_BASE_FOLDER = "PLACEHOLDER"


def process_collage_images(image_urls: list, local=False):
    """
    Takes in a list of the user's images
    Filters k images and finds dominant color
    From filtered images, randomly select about 5-7 images to make collage
    Uploads these images to S3 (or locally store them)
    Returns list of stored image urls to be used in collage
    """
    p = PaletteFilter(local=local)
    (
        filtered_image_data,
        dominant_color,
        complementary_color,
    ) = p.filter_images(image_urls)

    # randomize list order
    random.shuffle(filtered_image_data)

    # select 75% of the images to make collage
    target_count = int(len(filtered_image_data) * PERCENT_CROPPED)
    current_count = 0
    cropped_image_urls = {}

    base_folder = LOCAL_BASE_FOLDER if local else S3_BASE_FOLDER

    for image_data in filtered_image_data:
        found_in_s3 = False
        if not local:
            # TODO: Check if cropped image already in S3,
            # if so, just change the url to a cropped url and
            # add to cropped url list (see code below)
            s3_cropped_url = get_cropped_name(
                image_data["url"], S3_BASE_FOLDER
            )
            ...
            # if the object is present in S3:
            # found_in_s3 = True

        if current_count >= target_count:
            break

        if not found_in_s3:
            # save image to S3
            cropped_image = extract_objects_from_image(
                image_data["url"], local=local
            )
            if cropped_image:
                saved_path = save_image_png(
                    cropped_image,
                    image_data["url"],
                    base_folder,
                    local=local,
                )
                current_count += 1
                cropped_image_urls[image_data["url"]] = saved_path
        else:
            cropped_image_urls[image_data["url"]] = s3_cropped_url

    cropped_image_data = [
        image_data
        for image_data in filtered_image_data
        if image_data["url"] in cropped_image_urls
    ]

    uncropped_image_data = [
        image_data
        for image_data in filtered_image_data
        if image_data["url"] not in cropped_image_urls
    ]

    for image_data in cropped_image_data:
        image_data["url"] = cropped_image_urls[image_data["url"]]

    return {
        "cropped_image_data": cropped_image_data,
        "uncropped_image_data": uncropped_image_data,
        "dominant_color": dominant_color,
        "complementary_color": complementary_color,
    }


if __name__ == "__main__":
    red_images = glob.glob("..\\tests\\red\\*")
    processed = process_collage_images(red_images, local=True)
    output_json_path = "..\\tests\\output.json"
    file = open(output_json_path, "w")
    json.dump(processed, file)
    pass
