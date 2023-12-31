import glob
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
import torchvision
from PIL import Image, ImageDraw, ImageFont
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
import numpy as np
from utils import get_cropped_name

CROPPED_CUTOFF_PERCENTAGE = 0.1


def extract_objects_from_image(image_path, local=False):
    # Load the pre-trained model for segmentation
    model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

    # Define the preprocessing pipeline
    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )
    if not local:
        response = requests.get(image_path)
        image_data = BytesIO(response.content)
        input_image = Image.open(image_data).convert("RGB")
    else:
        input_image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    # Check if a GPU is available and if not, use a CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_batch = input_batch.to(device)
    model.to(device)

    # Get the segmentation mask from the model
    with torch.no_grad():
        output = model(input_batch)["out"][0]
    output_predictions = torch.argmax(output, dim=0)

    # Create a binary mask
    mask = output_predictions.unsqueeze(2).expand(-1, -1, 3).byte().numpy()
    mask = Image.fromarray(mask)
    mask = mask.resize(input_image.size, Image.NEAREST).convert("L")

    # Count non-zero pixels in the mask
    mask_np = np.array(mask)
    non_zero_pixels = np.count_nonzero(mask_np)
    percentage_of_non_zero_pixels = non_zero_pixels / (
        mask_np.shape[0] * mask_np.shape[1]
    )
    print("True pixel count:", percentage_of_non_zero_pixels, image_path)

    if percentage_of_non_zero_pixels < CROPPED_CUTOFF_PERCENTAGE:
        print("Not enough pixels to crop")
        return None

    # Convert the original image and mask to PyTorch tensors
    segmented_image_tensor = (
        transforms.ToTensor()(input_image).unsqueeze(0).to(device)
    )
    mask_tensor = transforms.ToTensor()(mask).unsqueeze(0).to(device)

    # Create an RGBA image tensor with the original colors and set the alpha channel using the mask
    alpha_channel = (mask_tensor > 0).float()
    rgba_image = torch.cat([segmented_image_tensor, alpha_channel], dim=1)

    # Convert the tensor back to an image and save
    segmented_image = transforms.ToPILImage()(rgba_image.squeeze(0))
    return segmented_image


def save_image_png(
    segmented_image, original_url, base_folder, local=False
):
    if not segmented_image:
        return
    output_path = get_cropped_name(original_url, base_folder)
    if local:
        segmented_image.save(output_path, "PNG")
    if not local:
        # TODO: Save to S3
        pass

    return output_path


def detect_objects(image_path, threshold=0.5):
    # Load a pre-trained model for object detection
    model = fasterrcnn_resnet50_fpn(pretrained=True).eval()

    # Load an image
    image = Image.open(image_path).convert("RGB")
    image_tensor = F.to_tensor(image).unsqueeze(0)

    # Get predictions from the model
    with torch.no_grad():
        predictions = model(image_tensor)

    # Filter predictions with confidence scores above the threshold
    high_confidence_predictions = []
    for prediction in predictions:
        keep_boxes = prediction["scores"] > threshold
        high_confidence_predictions.append(
            {
                "boxes": prediction["boxes"][keep_boxes].cpu().numpy(),
                "labels": prediction["labels"][keep_boxes].cpu().numpy(),
                "scores": prediction["scores"][keep_boxes].cpu().numpy(),
            }
        )

    return high_confidence_predictions


def draw_boxes(image_path, predictions, output_path=None, threshold=0.5):
    # Load the image
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Set the size of the text box
    text_height = 10  # Approximate height of the text box
    text_margin = 5  # Small margin around the text for better visibility

    # Draw the bounding boxes and labels on the image
    for element in predictions:
        for box, label, score in zip(
            element["boxes"], element["labels"], element["scores"]
        ):
            if score >= threshold:
                # Draw the box
                box_coords = tuple(box)
                draw.rectangle(box_coords, outline="red", width=3)

                # Draw the label and score as text
                text = f"{label} {score:.2f}"
                text_width = (
                    len(text) * 6
                )  # Estimate text width based on character count
                # Draw a filled rectangle behind the text for better readability
                text_background = (
                    box_coords[0],
                    box_coords[1] - text_height - text_margin * 2,
                    box_coords[0] + text_width + text_margin * 2,
                    box_coords[1],
                )
                draw.rectangle(text_background, fill="red")
                draw.text(
                    (
                        box_coords[0] + text_margin,
                        box_coords[1] - text_height - text_margin,
                    ),
                    text,
                    fill="white",
                )

    # Display the image
    # image.show()
    # Optionally, save the image
    if output_path:
        image.save(output_path)


def main():
    urls = glob.glob("..\\tests\\red\\*")
    # end the file with png and save in tests/red-extract folder
    output_urls = [url.replace("red", "red-extract") for url in urls]
    for url, output_url in zip(urls, output_urls):
        print("Extracting objects from:", url)
        extract_objects_from_image(url, output_url, local=True)


if __name__ == "__main__":
    main()
