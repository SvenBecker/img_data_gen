"""This module is responsible for image transformation."""
from typing import TYPE_CHECKING, Tuple
from dataclasses import dataclass

import random

from img_data_gen.loaders import BoundingBox

if TYPE_CHECKING:
    from PIL import Image

class ImageRotator:

    def __init__(self, image: 'Image') -> None:
        self.image = image
        self.bounding_box = BoundingBox.from_img(image)

    def rnd_rotate(self) -> Tuple['Image', 'BoundingBox']:
        rotation: int = random.randint(0, 359)
        return self.image.rotate(rotation, expand=True), self.bounding_box.rotate(angle=rotation)

