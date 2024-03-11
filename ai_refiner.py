import os
import argparse

import lib.utils as utils
from lib.ai import DiffusionStrategy, RefinerStrategy
from PIL import Image


def is_image(path: str):
    allowed_extensions = ["jpg", "jpeg", "png"]

    _, ext = os.path.basename(path).split(".")

    if ext.lower() not in allowed_extensions:
        return False

    return True


def main(args):
    strategy: DiffusionStrategy = RefinerStrategy()

    pipeline = strategy.pipeline(
        # model_id="stabilityai/stable-diffusion-2",
        model_id="stabilityai/stable-diffusion-xl-refiner-1.0",
        use_safetensors=True,
    )

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"The image path '{args.input}' does not exist.")

    if not is_image(args.input):
        raise ValueError("The image file must have one of the supported extensions")

    image = Image.open(args.input).convert("RGB")

    output = strategy.execute(
        pipeline,
        image=[image],
        prompt="Increase image quality and make it detailed",
        width=728,
        height=1024,
        num_images_per_prompt=1,
        num_inference_steps=40,
        high_noise_frac=0.8,
        negative_prompt="bad quality",
    )

    if output:
        utils.save_images(
            output,
            prompt="Increase image quality and make it detailed",
            folder_path=args.output,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    file_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(file_path)

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The path to the file which you'd like to refine with AI tool",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=os.path.join(directory_path, "output"),
        help="The path to declare output of the refined images",
    )

    args = parser.parse_args()

    main(args)
