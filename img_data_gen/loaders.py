from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Tuple, List, Dict

from PIL import Image

from img_data_gen.constants import INPUT_IMG_FOLDER, BACKGROUND_IMG_FOLDER


@dataclass
class ImageContainer:
    input_image_map: Dict[str, 'Image']
    bg_image_list: List['Image']


@dataclass
class ImageLoader:
    input_img_folder: Path = INPUT_IMG_FOLDER
    background_image_folder: Path = BACKGROUND_IMG_FOLDER
    input_img_size: Tuple[int, int] = (int(800 * 0.7140232700551132), 800)

    def load_all(self) -> ImageContainer:
        input_image_fps: List[Path] = list(self.input_img_folder.glob('*.jpg'))

        with ThreadPoolExecutor() as executor:
            input_futures = [
                executor.submit(self._load_input_image, filepath)
                for filepath in input_image_fps
            ]
            bg_futures = [
                executor.submit(self._load_bg_image, filepath)
                for filepath in self.background_image_folder.glob('*.jpg')
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
