"""This module is responsible for image transformation."""
from typing import TYPE_CHECKING, Tuple
from dataclasses import dataclass

import random

from img_data_gen.loaders import BoundingBox

if TYPE_CHECKING:
    from PIL import Image


def rnd_transform(img: 'Image') -> 'Image':
    rotation: int = random.randint(0, 359)
    return img.rotate(rotation, expand=True)


class ImageTransformer:

    def __init__(self, image: 'Image') -> None:
        self.image = image
        self.bounding_box = BoundingBox.from_img(image)

    def rnd_transform(self) -> Tuple['Image', 'BoundingBox']:
        rotation: int = random.randint(0, 359)
        return self.image.rotate(rotation, expand=True), self.bounding_box.rotate(angle=rotation)

