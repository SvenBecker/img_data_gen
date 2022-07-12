from typing import Tuple, List

from PIL import Image

from img_data_gen.constants import INPUT_IMG_FOLDER


def load_all_images(size: Tuple[int, int] = (int(800 * 0.7140232700551132), 800)) -> List['Image']:
    return [
        Image.open(filepath).convert('RGBA').resize(size)
        for filepath in INPUT_IMG_FOLDER.glob('*.jpg')
    ]
