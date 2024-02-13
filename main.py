import os
import random
import time
import argparse

from lib.uploader import Uploader
import lib.utils as utils


def find_partially_matching_folders(images_folder, authors):
    partially_matching_folders = []
    for author in authors:
        for folder in os.listdir(images_folder):
            if author.lower().replace(" ", "_") in folder.lower():
                author_folder = os.path.join(images_folder, folder)
                partially_matching_folders.append(author_folder)
                break
    return partially_matching_folders


def main(authors):
    try:
        formatted_authors = utils.format_author_names(authors)
        author_folders = find_partially_matching_folders("images", formatted_authors)
        all_works = utils.get_files_from_folders(author_folders)
        prepared_works = utils.prepare_elements(all_works, max_files=2)

        assert prepared_works, "There are no works collected..."

        while prepared_works:
            element_path = prepared_works[0]
            content = element_path.replace("images/", "").replace(".png", "")
            caption = utils.format_content(content)

            print(caption)

            Uploader.story()

            del prepared_works[0]

            time.sleep(5 * 60)

        print("The uploading successfully completed")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "-a",
        "--authors",
        nargs="+",
        default=["Artifactual Intelligence"],
        help="List of authors to process",
    )
    args = parser.parse_args()

    main(args.authors)
