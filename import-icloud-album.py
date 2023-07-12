#!python3
# This script fetches all the photos from a shared iCloud photo album, saves them to the static/photo
# directory, and then generates Hugo shortcodes for those photos.
# It does not require any authentication, but it does require the album to be shared with you via a link.
# Based on TypeScript code from https://github.com/ghostops/ICloud-Shared-Album
import argparse
import json
import os
import shutil
from datetime import datetime
from urllib import request

# iCloud HTTP headers
headers = {
    "Origin": "https://www.icloud.com",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Content-Type": "text/plain",
    "Accept": "*/*",
    "Referer": "https://www.icloud.com/sharedalbum/",
    "Connection": "keep-alive",
}


# Derivative represents an image in a specific size.
class Derivative:
    def __init__(self, checksum: str, file_size: int, width: int, height: int, url: str = None):
        self.checksum = checksum
        self.file_size = file_size
        self.width = width
        self.height = height
        self.url = url

    # Static method to create a Derivative from a dictionary.
    @staticmethod
    def from_dict(data: dict):
        return Derivative(
            checksum=data["checksum"],
            file_size=int(data["fileSize"]),
            width=int(data["width"]),
            height=int(data["height"]),
            url=data["url"] if "url" in data else None,
        )

    # Returns dictionary representation of the derivative.
    def to_dict(self):
        return {
            "checksum": self.checksum,
            "fileSize": self.file_size,
            "width": self.width,
            "height": self.height,
            "url": self.url,
        }


# Image represents a photo in the album in iCloud.
class Image:
    def __init__(
        self,
        batch_guid: str,
        derivatives: dict[str, Derivative],
        contributor_last_name: str,
        batch_date_created: str,
        date_created: str,
        contributor_first_name: str,
        photo_guid: str,
        contributor_full_name: str,
        caption: str,
        height: int,
        width: int,
        media_asset_type: str = None
    ):
        self.batch_guid = batch_guid
        self.derivatives = derivatives
        self.contributor_last_name = contributor_last_name
        self.batch_date_created = batch_date_created
        self.date_created = date_created
        self.contributor_first_name = contributor_first_name
        self.photo_guid = photo_guid
        self.contributor_full_name = contributor_full_name
        self.caption = caption
        self.height = height
        self.width = width
        self.media_asset_type = media_asset_type

    # Static method to create an Image from a dictionary.
    @staticmethod
    def from_dict(data: dict):
        derivatives = {
            key: Derivative.from_dict(value) for key, value in data["derivatives"].items()
        }
        return Image(
            batch_guid=data["batchGuid"],
            derivatives=derivatives,
            contributor_last_name=data["contributorLastName"],
            batch_date_created=data["batchDateCreated"],
            date_created=data["dateCreated"],
            contributor_first_name=data["contributorFirstName"],
            photo_guid=data["photoGuid"],
            contributor_full_name=data["contributorFullName"],
            caption=data["caption"],
            height=int(data["height"]),
            width=int(data["width"]),
            media_asset_type=data["mediaAssetType"] if "mediaAssetType" in data else None,
        )

    # Returns dictionary representation of the image.
    def to_dict(self):
        return {
            "batchGuid": self.batch_guid,
            "derivatives": {
                key: value.to_dict() for key, value in self.derivatives.items()
            },
            "contributorLastName": self.contributor_last_name,
            "batchDateCreated": self.batch_date_created,
            "dateCreated": self.date_created,
            "contributorFirstName": self.contributor_first_name,
            "photoGuid": self.photo_guid,
            "contributorFullName": self.contributor_full_name,
            "caption": self.caption,
            "height": self.height,
            "width": self.width,
            "mediaAssetType": self.media_asset_type,
        }

    # Returns a dict containing the URL, width and height of the derivative with the same height
    # as the image itself.
    def get_original(self) -> dict | None:
        for derivative in self.derivatives.values():
            if derivative.height == self.height:
                return {
                    "checksum": derivative.checksum,
                    "url": derivative.url,
                    "width": derivative.width,
                    "height": derivative.height,
                }
        return None

    # Returns a dict containing the URL, width and height of the smallest derivative.
    def get_smallest_derivative(self) -> dict | None:
        smallest_derivative = None
        for derivative in self.derivatives.values():
            if smallest_derivative is None or derivative.height < smallest_derivative.height:
                smallest_derivative = derivative
        return {
            "checksum": smallest_derivative.checksum,
            "url": smallest_derivative.url,
            "width": smallest_derivative.width,
            "height": smallest_derivative.height,
        }


# Metadata represents metadata for the album.
class Metadata:
    def __init__(
        self,
        stream_name: str,
        user_first_name: str,
        user_last_name: str,
        stream_ctag: str,
        items_returned: int,
        locations: dict
    ):
        self.stream_name = stream_name
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.stream_ctag = stream_ctag
        self.items_returned = items_returned
        self.locations = locations

    # Static method to create Metadata from a dictionary.
    @staticmethod
    def from_dict(data: dict):
        return Metadata(
            stream_name=data["streamName"],
            user_first_name=data["userFirstName"],
            user_last_name=data["userLastName"],
            stream_ctag=data["streamCtag"],
            items_returned=data["itemsReturned"],
            locations=data["locations"],
        )

    # Returns dictionary representation of the metadata.
    def to_dict(self):
        return {
            "streamName": self.stream_name,
            "userFirstName": self.user_first_name,
            "userLastName": self.user_last_name,
            "streamCtag": self.stream_ctag,
            "itemsReturned": self.items_returned,
            "locations": self.locations,
        }


# ApiResponse represents the response from the iCloud API.
class ApiResponse:
    def __init__(
        self,
        photos: dict[str, Image],
        photo_guids: list[str],
        metadata: Metadata
    ):
        self.photos = photos
        self.photo_guids = photo_guids
        self.metadata = metadata


# Album represents the response from the iCloud API.
class Album:
    def __init__(
        self,
        token: str,
        metadata: Metadata,
        images: list[Image]
    ):
        self.token = token
        self.metadata = metadata
        self.images = images


# This functions gets a link to shared album json data using an album token.
# The token is the last part of the URL when you open the album in a browser.
def get_base_url(token):
    BASE_62_CHAR_SET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def base62_to_int(e):
        t = 0
        for char in e:
            t = t * 62 + BASE_62_CHAR_SET.index(char)
        return t

    e = token
    t = e[0]
    n = base62_to_int(e[1]) if t == 'A' else base62_to_int(e[1:3])
    i = e.find(';')
    r = e
    s = None

    if i >= 0:
        s = e[i + 1:]
        r = r.replace(';' + s, '')

    server_partition = n

    base_url = f'https://p{server_partition:02d}-sharedstreams.icloud.com/{token}/sharedstreams/'

    return base_url


# get_api_response returns a web stream response for a shared album.
def get_api_response(base_url: str):
    url = base_url + "webstream"
    data = {"streamCtag": None}
    data_string = json.dumps(data).encode("utf-8")
    req = request.Request(url, headers=headers,
                          data=data_string, method="POST")
    with request.urlopen(req) as response:
        response_data = response.read().decode("utf-8")

    data = json.loads(response_data)
    photos: dict[str, Image] = {}
    photo_guids: list[str] = []

    for photo in data["photos"]:
        photos[photo["photoGuid"]] = Image.from_dict(photo)
        photo_guids.append(photo["photoGuid"])

    return ApiResponse(
        photos=photos,
        photo_guids=photo_guids,
        metadata=Metadata(
            stream_name=data["streamName"],
            user_first_name=data["userFirstName"],
            user_last_name=data["userLastName"],
            stream_ctag=data["streamCtag"],
            items_returned=int(data["itemsReturned"]),
            locations=data["locations"],
        ),
    )


# get_urls returns a dictionary of image URLs for the given photo GUIDs.
def get_urls(base_url: str, photo_guids: list[str]):
    url = base_url + "webasseturls"
    data = {"photoGuids": photo_guids}
    data_string = json.dumps(data).encode("utf-8")
    print(f"Retrieving URLs for {photo_guids[0]} - {photo_guids[-1]}...")
    req = request.Request(url, headers=headers,
                          data=data_string, method="POST")
    with request.urlopen(req) as response:
        response_data = response.read().decode("utf-8")

    data = json.loads(response_data)
    items = {}

    for item_id, item in data["items"].items():
        items[item_id] = "https://" + item["url_location"] + item["url_path"]

    return items


# parse_date parses a date string into a datetime object.
def parse_date(date: str | None) -> datetime | None:
    if not date:
        return None

    try:
        return datetime.fromisoformat(date)
    except ValueError:
        return None


# enrich_images_with_urls adds real image URLs to the Image objects.
def enrich_images_with_urls(api_response: ApiResponse, urls: dict[str, str]) -> list[Image]:
    photos_with_derivative_urls = []

    for guid, photo in api_response.photos.items():
        # print(f'Enriching {guid} with URLs', photo.to_dict())
        derivatives_by_height = {}
        duplicate_derivative_count = {}

        for key, derivative in photo.derivatives.items():
            # print(f'Enriching derivative {key} with URL', derivative.to_dict())
            if derivative.checksum not in urls:
                continue

            derivative_key = str(derivative.height)

            if derivative_key in derivatives_by_height:
                if derivative_key not in duplicate_derivative_count:
                    duplicate_derivative_count[derivative_key] = 1
                else:
                    duplicate_derivative_count[derivative_key] += 1

                derivative_key = derivative_key + '-' + \
                    duplicate_derivative_count[derivative_key]

            derivative.url = urls[derivative.checksum]
            derivatives_by_height[derivative_key] = derivative

        photo.derivatives = derivatives_by_height
        photos_with_derivative_urls.append(photo)

    return photos_with_derivative_urls


# chunks splits a list into chunks of a given size.
def chunks(lst: list, n: int) -> list:
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


# this function gets album token after # in URLs like 'https://www.icloud.com/sharedalbum/#B0NJtdOXm9LvzZ'
def get_album_token(url: str) -> str:
    return url.split('#')[1]


# Fetches all images from a shared album with a given token.
# It uses base_url to fetch the images, splits all photo_guids into chunks of
# 20 and then fetches all image URLs for each chunk. After that it enriches
# the Image objects with the URLs and returns them together with album metadata.
def get_album_with_images(token: str) -> Album:
    base_url = get_base_url(token)
    api_response = get_api_response(base_url)
    photo_guids = api_response.photo_guids
    images = []
    urls = {}

    for chunk in chunks(photo_guids, 20):
        urls.update(get_urls(base_url, chunk))

    images = enrich_images_with_urls(api_response, urls)

    return Album(
        token=token,
        metadata=api_response.metadata,
        images=images,
    )


# Photo represents a single photo with a thumbnail that can be downloaded and saved.
class Photo:
    def __init__(
        self,
        checksum: str,
        url: str,
        width: int,
        height: int,
        thumb_url: str,
        thumb_width: int,
        thumb_height: int,
        author: str | None = None,
        caption: str | None = None,
    ):
        self.checksum = checksum
        self.url = url
        self.width = width
        self.height = height
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        self.author = author
        self.caption = caption

    @staticmethod
    def from_image(image: Image):
        source = image.get_original()
        thumb = image.get_smallest_derivative()

        return Photo(
            checksum=source["checksum"],
            url=source["url"],
            width=source["width"],
            height=source["height"],
            thumb_url=thumb["url"],
            thumb_width=thumb["width"],
            thumb_height=thumb["height"],
            author=image.contributor_full_name,
            caption=image.caption,
        )

    def to_dict(self) -> dict:
        return {
            "checksum": self.checksum,
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "thumb_url": self.thumb_url,
            "thumb_width": self.thumb_width,
            "thumb_height": self.thumb_height,
            "author": self.author,
            "caption": self.caption,
        }


def download_file(url: str, path: str):
    req = request.Request(url, headers=headers)
    with request.urlopen(req) as response, open(path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


# Given an URL like extracts the file name part from it, skipping the query string part. Casts it to lower case and returns.
def get_file_name_from_url(url: str) -> str:
    return url.split('?')[0].split('/')[-1].lower()


def get_download_file_name(photo: Photo, token: str, directory: str) -> str:
    file_name = get_file_name_from_url(photo.url)
    base_name, extension = os.path.splitext(file_name)
    file_name = f'{base_name}-{photo.checksum}{extension}'
    file_path = f'{directory}/{token}/{file_name}'

    return file_path


# Downloads a photo if it doesn't exist in the target directory already.
# Takes checksum into account to avoid overwriting existing files and downloading unnecessary ones.
def download_photo(photo: Photo, token: str, directory: str):
    file_path = get_download_file_name(photo, token, directory)

    if not os.path.exists(f'{directory}/{token}'):
        os.makedirs(f'{directory}/{token}')

    if not os.path.exists(file_path):
        print(f'Downloading {file_path} from {photo.url}')
        download_file(photo.url, file_path)


def get_photo_shortcode(photo: Photo, token: str, directory: str, width: int) -> str:
    file_path = get_download_file_name(photo, token, directory)
    height = photo.height
    if width:
        aspect_ratio = photo.width / photo.height
        height = int(width / aspect_ratio)
    else:
        width = photo.width

    # Copy the part after the first slash to ignore the Hugo-specific folder
    src = file_path.split('/', maxsplit=1)[1]
    shortcode = f'{{{{<photo src="{src}" caption="{photo.caption}" width="{width}" height="{height}" src-width="{photo.width}" src-height="{photo.height}" >}}}}'

    return shortcode


# Get token from command line argument using argparse
parser = argparse.ArgumentParser(
    description='Imports iCloud shared album images to assets/photo and prints Hugo shortcodes for them')
parser.add_argument('token', metavar='TOKEN', type=str,
                    help='iCloud Shared Album token')
parser.add_argument('directory', metavar='DIRECTORY', type=str, nargs='?',
                    default='assets/photo', help='Target directory to save files in. Default: assets/photo')
parser.add_argument('-w', '--width', type=int, help='Thumbnail width')
args = parser.parse_args()

token = args.token

album = get_album_with_images(args.token)
# print(json.dumps(album.metadata.to_dict(), sort_keys=True, indent=4))
shortcodes = []
for image in album.images:
    photo = Photo.from_image(image)
    # print(json.dumps(photo.to_dict(), sort_keys=True,
    #       indent=4, separators=(',', ': ')))
    download_photo(photo, token, args.directory)
    shortcodes.append(get_photo_shortcode(
        photo, token, args.directory, args.width))

print('Shortcodes for the imported images:')
print('---\n')
print('\n\n'.join(shortcodes))
