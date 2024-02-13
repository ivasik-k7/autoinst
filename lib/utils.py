import os
import random
from typing import List
from PIL import Image


def format_author_names(author_strings: List[str]) -> List[str]:
    return [
        "_".join(word.lower() for word in author.split()) for author in author_strings
    ]


def get_files_from_folders(folders: List[str]) -> List[str]:
    all_files = []
    for folder in folders:
        folder_files = [
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, file))
        ]
        all_files.extend(folder_files)
    return all_files


def prepare_elements(files: List[str], max_files: int = 7) -> List[str]:
    random.shuffle(files)
    return files[:max_files]


def format_content(template: str) -> str:
    parts = template.split("/")
    author = parts[0].replace("_", " ").title()
    work_name = parts[1].replace("_", " ").title()
    return f"{author} - {work_name}"


def save_images(
    images: list,
    folder_path: str,
    prompt: str,
):
    os.makedirs(folder_path, exist_ok=True)

    words = prompt.split()
    short_name = "".join(word[:3] for word in words if word.isalpha())[:12].lower()

    for i, image in enumerate(images):
        image_name = get_unique_filename(folder_path, f"{short_name}.png")
        print(image_name)
        image.save(os.path.join(folder_path, image_name))


def get_unique_filename(folder, filename):
    if os.path.exists(os.path.join(folder, filename)):
        base, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_filename = f"{base}_{counter}{ext}"
            if not os.path.exists(os.path.join(folder, new_filename)):
                return new_filename
            counter += 1
    else:
        return filename


def append_to_file(filename, text):
    with open(filename, "a+") as file:
        file.seek(0)  # Move to the beginning of the file
        data = file.read(100)  # Read some data to check if the file is empty
        if len(data) > 0:
            file.write("\n")  # If file is not empty, add a new line
        file.write(text)  # Append the text to the file
