import requests
import urllib.request
import os
import random
from dotenv import load_dotenv
import sys


def get_response(url, payload):
    try:
        response = requests.get(url, params=payload)
        response.raise_for_status()
    except requests.HTTPError:
        sys.stderr.write("Error with URL\n")

    return response


def get_url_to_upload(token, group_id):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload = {
        "access_token": token,
        "group_id": group_id,
        "v": "5.124"
    }
    response = get_response(url, payload)
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
        image_server = image_on_server["server"]
        image_hash = image_on_server["hash"]
        photo = image_on_server["photo"]
        return image_server, image_hash, photo


def save_comic(image_server, image_hash, photo, token, group_id):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    payload = {
        "access_token": token,
        "server": image_server,
        "hash": image_hash,
        "photo": photo,
        "group_id": group_id,
        "v": "5.124"
    }

    response = get_response(url, payload)
    saved_image = response.json()["response"][0]
    owner_id = saved_image["owner_id"]
    media_id = saved_image["id"]

    return owner_id, media_id


def post_comic(owner_id, media_id, token, comment, group_id):
    url = "https://api.vk.com/method/wall.post"
    payload = {
        "access_token": token,
        "v": "5.124",
        "owner_id": "-{}".format(group_id),
        "message": comment,
        "from_group": "1",
        "attachments": "photo{}_{}".format(owner_id, media_id)
    }
    get_response(url, payload)


def get_last_comic_number():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    last_comic_number = response.json()["num"]
    return last_comic_number


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    group_id = "198809484"
    last_comic_number = get_last_comic_number()
    url = "http://xkcd.com/{}/info.0.json".format(
        random.randint(1, last_comic_number))
    response = get_response(url, payload={})
    comic = response.json()
    image = urllib.request.urlopen(comic["img"])
    comment = comic["alt"]
    filename = "xkcd.png"

    try:
        with open(filename, "wb") as file:
            content = image.read()
            file.write(content)

        url_to_upload = get_url_to_upload(token, group_id)
        image_server, image_hash, photo = upload_comic_to_server(url_to_upload)
        owner_id, media_id = save_comic(
            image_server, image_hash, photo, token, group_id)
        post_comic(owner_id, media_id, token, comment, group_id)

    finally:
        os.remove(filename)


if __name__ == "__main__":
    main()
