from bs4 import BeautifulSoup
import requests
import os
import re


AUCTIONS_MAX_COUNT: int = 25


def sanitize_filename(filename):
    return re.sub(r"[^\w\-_. ]", "", filename)


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


def write_image_from_url(url, folder, filename):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as file:
                file.write(response.content)

            print("Image successfully saved:", file_path)
        else:
            print("Failed to fetch image from URL:", url)
    except Exception as e:
        print("Error occurred while fetching image:", e)


def fetch_page_content(url: str):
    response = requests.get(url)

    response.raise_for_status()

    return response.text


def parse_html_content(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")

    post_elements = soup.find_all(
        lambda tag: tag.has_attr("alt") and tag.has_attr("data-srcset")
    )

    for element in post_elements:
        try:
            post_url = element.attrs.get("data-src", "")
            post_description = element.attrs.get("alt", "Unknown")

            author, title = map(str.strip, post_description.split(","))

            author_name = author.strip().lower().replace(" ", "_")
            author_folder_path = os.path.join("images", author_name)

            os.makedirs(author_folder_path, exist_ok=True)

            sanitized_title = (
                sanitize_filename(title.lower().strip().replace(" ", "_")) + ".png"
            )
            unique_file_name = get_unique_filename(author_folder_path, sanitized_title)

            write_image_from_url(post_url, author_folder_path, unique_file_name)
        except Exception as e:
            print("Error occurred:", e)


def main():
    for i in range(15, 21):
        url_template = (
            f"https://resslerkunst.com/kataloge/?_sft_product_cat={i}-kunstauktion"
        )

        html_content = fetch_page_content(url_template)

        parse_html_content(html_content)


main()
