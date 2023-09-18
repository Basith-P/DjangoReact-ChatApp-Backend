from django.core.exceptions import ValidationError
from PIL import Image


def validate_icon_size(image):
    img = Image.open(image)
    if img.width > 128 or img.height > 128:
        raise ValidationError(
            "Image size must be 128x128 or less")


def validate_image_extension(image):
    valid = ('.png', '.jpg', '.jpeg')
    if not image.name.endswith(valid):
        raise ValidationError(
            "Image must be a PNG or JPG/JPEG file")
