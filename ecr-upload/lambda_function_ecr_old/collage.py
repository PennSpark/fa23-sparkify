import json
from palette import PaletteFilter
from extractor import extract_objects_from_image, save_image_png
import random
import glob
import os
import boto3
from io import BytesIO
from PIL import Image
from pprint import pprint
from utils import get_cropped_name
from urllib.parse import urlparse



PERCENT_CROPPED = 0.6
LOCAL_BASE_FOLDER = "..\\tests\\red-extract"
S3_BASE_FOLDER = ""
S3_BUCKET_NAME = "fa23-sparkify-bucket"
s3 = boto3.client('s3')

def is_image_in_s3(image_url, bucket_name):
    # Extract object key from the image URL
    print("HIIIIIII: " + image_url) 
    parsed_url = urlparse(image_url)
    print("HIIIIIII: " + parsed_url.path) 
    path_components = parsed_url.path.split("/")
    object_key = os.path.basename(path_components[-1]) + ".png"

    # Check if the object exists in the S3 bucket
    try:
        s3.head_object(Bucket=bucket_name, Key=object_key)
        print('OBJECT IN BUCKET')
        return True  # Object exists
    except Exception as e:
        if '404' in str(e):  # S3 returns a 404 error if the object is not found
            return False  # Object does not exist
        else:
            raise  # Propagate other exceptions

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
            if is_image_in_s3(image_data["url"], S3_BUCKET_NAME):
                s3_cropped_url = get_cropped_name(
                    image_data["url"], S3_BASE_FOLDER
                )
                ...
                # if the object is present in S3:
                found_in_s3 = True

        if current_count >= target_count:
            break

        if not found_in_s3:
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
    #red_images = glob.glob("..\\tests\\red\\*")
    red_images = ["https://i.scdn.co/image/ab67616d00001e02fb1808a11a086d2ba6edff51",
                  "https://i.scdn.co/image/ab6761610000e5eb95cc5cc99f557587636f7f29"]
    print(red_images)
    processed = process_collage_images(red_images, local=False)
    output_json_path = "..\\tests\\output.json"
    file = open(output_json_path, "w")
    json.dump(processed, file)
    pass
