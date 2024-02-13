import configparser
from instagrapi import Client

config = configparser.ConfigParser()
config.read("config.ini")

assert (
    "credentials" in config
), "Credentials section not found in the configuration file."


login = config["credentials"]["login"]
password = config["credentials"]["password"]

assert login, "Login not obtained successfully."
assert password, "Password not obtained successfully."


class Uploader:
    @staticmethod
    def story(path: str, caption: str):
        print(f"Uploading element: {caption}")

        cl = Client()

        cl.login(login, password)

        cl.photo_upload_to_story(path, caption=caption)
