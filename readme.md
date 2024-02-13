# AI Image Generation and Upload

This repository contains scripts for generating AI-generated images using [DiffusionGenerator](https://github.com/stabilityai/diffusion), and uploading them to social media platforms like Instagram using Uploader.

## Dependencies

This project uses [Poetry](https://python-poetry.org/) for managing dependencies. Install dependencies using the following command:

```bash
pip install poetry

poetry install
```

## Usage

### Image Generation

To generate AI-generated images, run the following command:

```bash
python ai_main.py --prompt "Your prompt here" --num_interfaces 25 --num_images 1 --negative_prompt "" --height 1024 --width 576
```

### Image Upload

To upload generated images to social media platforms, run the following command:

```bash
python main.py -a "Artifactual Intelligence"
```

You can specify one or more authors using the `-a` or `--authors` option.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
