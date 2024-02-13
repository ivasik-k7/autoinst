import cv2
import os
import argparse
from enum import Enum
from PIL import Image, ImageEnhance, ImageFilter


class UpscaleCategory(Enum):
    default = 1
    x2 = 2
    x3 = 3
    x4 = 4


# TODO LIST

# реалізувати ступіть upscaling
# реалізувати механізм аргрументів
# підібрати еффективний фільтр для покращення контрасності (якості зображення)
# a. підвищенні рівень DPI (Inch per Pixel)
# b.


def is_image(file_path):
    image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]

    _, extension = os.path.splitext(file_path)
    if extension.lower() in image_extensions:
        return True
    else:
        return False


def find_images(input_dir):
    files = []

    if os.path.exists(input_dir):

        for file in os.listdir(input_dir):

            if is_image(file):
                files.append(os.path.join(input_dir, file))

    else:
        print(f"Directory '{input_dir}' does not exist.")

    return files


def resize_by_coefficient(image, coefficient):
    new_width = int(image.width * coefficient)
    new_height = int(image.height * coefficient)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    return resized_image


def enhance_characteristics(file_path: str) -> Image:
    image = Image.open(file_path)

    image = ImageEnhance.Sharpness(image).enhance(3)
    image = ImageEnhance.Color(image).enhance(3)
    image = ImageEnhance.Brightness(image).enhance(0.98)

    return image


def save_image(image, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, filename)

    image.save(file_path, dpi=(300, 300), quality=95)


def main(
    upscale_value: UpscaleCategory,
    input_dir: str,
    output_dir: str,
) -> None:
    images = find_images(input_dir)

    print(images)

    for path in images:
        filename = os.path.basename(path)

        image = enhance_characteristics(path)
        image = resize_by_coefficient(image, upscale_value.value)

        save_image(image, output_dir, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument(
        "-u",
        "--upscale",
        type=int,
        choices=[state.value for state in UpscaleCategory],
        default=1,
        help="Upscale value (1, 2, 3, or 4)",
    )

    parser.add_argument(
        "--input-dir",
        "-i",
        type=str,
        default="{}/input".format(os.path.abspath(__file__)),
        help="Input directory for images (default: input)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="{}/output".format(os.path.abspath(__file__)),
        help="Output directory for images (default: output)",
    )

    args = parser.parse_args()

    upscale_value = UpscaleCategory(args.upscale)
    input_dir = args.input_dir
    output_dir = args.output_dir

    main(
        upscale_value,
        input_dir=input_dir,
        output_dir=output_dir,
    )
