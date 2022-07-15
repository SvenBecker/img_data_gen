"""This module is responsible for image loading."""
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Tuple, List, Dict

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
        # todo[high]: probably also resize the background image and select one with a lower resolution
        return Image.open(filepath).convert('RGBA')
