import requests
import urllib.request
import os
from dotenv import load_dotenv
load_dotenv()


def get_url_to_upload(token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    payload = {
        "access_token": token,
        "group_id": "198809484",
        "v": "5.124"
    }
    response = requests.get(url, params=payload)
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
    print(response.url)


def main():
    token = os.getenv("ACCESS_TOKEN")
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image = urllib.request.urlopen(comic["img"])

    with open("xkcd.png", "wb") as file:
        content = image.read()
        file.write(content)

    url_to_upload = get_url_to_upload(token)
    image_on_server = upload_comic_to_server(url_to_upload)
    save_comic(image_on_server, token)


if __name__ == "__main__":
    main()
