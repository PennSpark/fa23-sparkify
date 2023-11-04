import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO


def extract_objects_from_image(image_path, output_path, isLocal=False):
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
    if not isLocal:
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
    segmented_image.save(output_path, "PNG")


# Test the function
# extract_objects_from_image("nirvana.jpeg", "nirvana.png")
extract_objects_from_image(
    "https://hips.hearstapps.com/hmg-prod/images/cutest-dog-breed-bernese-64356a43dbcc5.jpg",
    "url.png",
)
