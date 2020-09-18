import requests
import urllib.request


def main():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image = urllib.request.urlopen(comic["img"])
    print(comic["alt"])
    with open("xkcd.png", "wb") as file:
        content = image.read()
        file.write(content)


if __name__ == "__main__":
    main()
