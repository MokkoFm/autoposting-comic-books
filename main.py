import requests
import urllib.request
import os
import random
from dotenv import load_dotenv


def get_url_to_upload(token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload = {
        "access_token": token,
        "group_id": "198809484",
        "v": "5.124"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    url_to_upload = response.json()["response"]["upload_url"]
    return url_to_upload


def upload_comic_to_server(url_to_upload):
    with open('xkcd.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url_to_upload, files=files)
        response.raise_for_status()
        image_on_server = response.json()
        return image_on_server


def save_comic(image_on_server, token):
    url_to_save = "https://api.vk.com/method/photos.saveWallPhoto"
    payload = {
        "access_token": token,
        "server": image_on_server["server"],
        "hash": image_on_server["hash"],
        "photo": image_on_server["photo"],
        "group_id": "198809484",
        "v": "5.124"
    }

    response = requests.get(url_to_save, params=payload)
    response.raise_for_status()
    saved_image = response.json()
    for image in saved_image["response"]:
        owner_id = image["owner_id"]
        media_id = image["id"]

    return owner_id, media_id


def post_comic(owner_id, media_id, token, comment):
    url_to_post = "https://api.vk.com/method/wall.post"
    payload = {
        "access_token": token,
        "v": "5.124",
        "owner_id": "-198809484",
        "message": comment,
        "from_group": "1",
        "attachments": "photo{}_{}".format(owner_id, media_id)
    }
    response = requests.get(url_to_post, params=payload)
    response.raise_for_status()


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    last_comic_number = 2359
    url = "http://xkcd.com/{}/info.0.json".format(
        random.randint(1, last_comic_number))
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image = urllib.request.urlopen(comic["img"])
    comment = comic["alt"]

    with open("xkcd.png", "wb") as file:
        content = image.read()
        file.write(content)

    url_to_upload = get_url_to_upload(token)
    image_on_server = upload_comic_to_server(url_to_upload)
    owner_id, media_id = save_comic(image_on_server, token)
    post_comic(owner_id, media_id, token, comment)


if __name__ == "__main__":
    main()
