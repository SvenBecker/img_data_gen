"""This module is responsible for image loading."""
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Tuple, List, Dict

import numpy as np
from PIL import Image


@dataclass
class ImageContainer:
    """Stores input and background image data."""
    input_image_map: Dict[str, 'Image']
    bg_image_list: List['Image']


@dataclass
class ImageLoader:
    """This class is responsible for loading images."""
    input_img_folder: Path
    bg_img_folder: Path
    input_img_size: Tuple[int, int] = (int(800 * 0.7140232700551132), 800)

    def load_all(self) -> ImageContainer:
        """Load all input and background images and stores the in some `ImageContainer` object."""
        input_image_fps: List[Path] = list(self.input_img_folder.glob('*.jpg'))

        with ThreadPoolExecutor() as executor:
            input_futures = [
                executor.submit(self._load_input_image, filepath)
                for filepath in input_image_fps
            ]
            bg_futures = [
                executor.submit(self._load_bg_image, filepath)
                for filepath in self.bg_img_folder.glob('*.jpg')
            ]

        return ImageContainer(
            input_image_map={
                fp.stem: input_future.result()
                for fp, input_future in zip(input_image_fps, input_futures)
            },
            bg_image_list=[bg_future.result() for bg_future in bg_futures]
        )

    def _load_input_image(self, filepath: Path) -> 'Image':
        return Image.open(filepath).convert('RGBA').resize(self.input_img_size)

    def _load_bg_image(self, filepath: Path) -> 'Image':
        return Image.open(filepath).convert('RGBA')


@dataclass
class BoundingBox:
    """Represents a card bounding box. Takes a non-rotated input image as parameter"""
    vertices: List[Tuple[int, int]]
    center: Tuple[int, int]

    @classmethod
    def from_img(cls, img: 'Image', anchor: Tuple[int, int] = (0, 0)) -> 'BoundingBox':
        """Returns a bounding box object based on provided image."""
        # todo: isn't it `... + img_size[1]` because otherwise I'll receive negative values?
        vertices: List[Tuple[int, int]] = [
            anchor,
            (anchor[0], anchor[1] - img.size[1]),
            (anchor[0] + img.size[0], anchor[1] - img.size[1]),
            (anchor[0] + img.size[0], anchor[1])
        ]
        center = (anchor[0] + img.size[0] / 2, anchor[1] - img.size[1] / 2)
        return cls(vertices=vertices, center=center)

    def move(self, x: int = 0, y: int = 0) -> 'BoundingBox':
        """
        Moves bounding box by specified amount. Positive directions: right/up and returns a new BoundingBox object.
        """
        vertices = [
            (vertex[0] + x, vertex[1] + y)
            for i, vertex in enumerate(self.vertices)
        ]
        center = (self.center[0] + x, self.center[1] + y)
        return BoundingBox(vertices=vertices, center=center)

    def rotate(self, angle: int) -> 'BoundingBox':
        """
        Rotates bounding box by specified angle in degrees, counterclockwise around its center and returns a new
        BoundingBox object.
        """

        # rotational matrix
        c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
        matrix = np.array([[c, -s], [s, c]])

        # transform coordinates to move rotation center to origin
        vertices_temp = np.array(self.vertices) - np.array(self.center)

        # perform rotation
        vertices_rotated = [
            matrix.dot(vertices_temp[i, :])
            for i in range(4)
        ]
        
        # reverse transform and reformat
        # rounding causes inaccuracies after multiple sequential rotations
        vertices_rotated = (vertices_rotated + np.array(self.center)).round(decimals=0).astype(int)
        vertices = [tuple(line) for line in vertices_rotated]

        return BoundingBox(vertices=vertices, center=self.center)
