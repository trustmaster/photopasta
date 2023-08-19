#!python3
# Reads image files from a specified directory and outputs shortcodes for those images.

import os
import re
from argparse import ArgumentParser

from PIL import Image

class Photo:
    def __init__(self, src: str, caption: str, width: int, height: int, thumb_width: int, thumb_height: int):
        self.src = src
        self.caption = caption
        self.width = width
        self.height = height
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


    def to_shortcode(self) -> str:
        shortcode = f'{{{{<photo src="{self.src}" caption="{self.caption}" width="{self.thumb_width}" height="{self.thumb_height}" src-width="{self.width}" src-height="{self.height}" >}}}}'

        return shortcode

def get_jpeg_files(directory: str) -> list[str]:
    if not os.path.exists(directory):
        return []
    files = os.listdir(directory)
    return [f for f in files if re.match(r'\.(jpg|jpeg|png)$', f, flags=re.IGNORECASE)]

def get_image_dimensions(path: str) -> tuple[int, int]:
    image = Image.open(path)
    return (image.width, image.height)


if __name__ == '__main__':
    parser = ArgumentParser(description='Reads image files from a specified directory and outputs shortcodes for those images')
    parser.add_argument('directory', metavar='DIRECTORY', type=str, help='Directory to search images for in')
    parser.add_argument('-w', '--width', type=int, help='Thumbnail width in pixels for width priority shortcodes (standalone)')
    parser.add_argument('-h', '--height', type=int, help='Thumbnail height in pixels for height priority shortcodes (gallery tiles)')

    args = parser.parse_args()
