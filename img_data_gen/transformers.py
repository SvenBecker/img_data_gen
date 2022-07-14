"""This module is responsible for image transformation."""
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from PIL import Image


def rnd_transform(img: 'Image') -> 'Image':
    rotation: int = random.randint(0, 359)
    return img.rotate(rotation, expand=True)
