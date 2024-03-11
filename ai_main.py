import argparse
import os

import lib.utils as utils

from lib.ai import DiffusionStrategy, GeneratorStrategy


def main(args):
    high_noise_frac = 0.8
    strategy: DiffusionStrategy = GeneratorStrategy()

    pipeline = strategy.pipeline(
        "stabilityai/stable-diffusion-2-1",
        use_safetensors=True,
    )

    utils.append_to_file("prompts.txt", args.prompt)

    for _ in range(args.num_images):
        images = strategy.execute(
            pipeline=pipeline,
            prompt=args.prompt,
            num_inference_steps=args.num_interfaces,
            negative_prompt=args.negative_prompt,
            high_noise_frac=high_noise_frac,
            height=args.height,
            width=args.width,
            num_images_per_prompt=1,
        )

        if images:
            ai_path = "images/artifactual_intelligence"

            utils.save_images(
                images=images,
                prompt=args.prompt,
                folder_path=ai_path,
            )

            # files = os.listdir(ai_path)

            # files = [
            #     file for file in files if os.path.isfile(os.path.join(ai_path, file))
            # ]

            # files.sort(
            #     key=lambda x: os.path.getmtime(os.path.join(ai_path, x)), reverse=True
            # )

            # last_added_file = os.path.join(ai_path, files[0])

            # print(last_added_file)

        # Uploader.story(last_added_file, "AIGenerated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate images using DiffusionGenerator."
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        help="Prompt for image generation",
    )

    parser.add_argument(
        "--num_interfaces",
        type=int,
        default=1,
        help="Number of inference steps",
    )
    parser.add_argument(
        "--num_images",
        type=int,
        default=1,
        help="Number of images to generate per prompt",
    )
    parser.add_argument(
        "--negative_prompt",
        type=str,
        default="bad quality, artifacts",
        help="Negative prompt for image generation",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Height of generated images",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=728,
        help="Width of generated images",
    )
    args = parser.parse_args()

    main(args)
