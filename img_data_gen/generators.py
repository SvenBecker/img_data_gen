import datetime as dt
from pathlib import Path
from typing import List
import random

from tqdm import tqdm
from PIL import Image

from img_data_gen.constants import BACKGROUND_IMG_FOLDER, OUTPUT_FOLDER
from img_data_gen.selectors import select_random_imgs
from img_data_gen.transformers import rnd_transform


def generate_image(
    img_permutation_lst: List['Image'],
    bg_img_path: Path = BACKGROUND_IMG_FOLDER / 'table1.jpg',
) -> 'Image':
    bg_img = Image.open(bg_img_path).convert('RGBA')
    for img in img_permutation_lst:
        img = rnd_transform(img)
        anchor1 = random.randint(0, bg_img.size[0] - img.size[0])
        anchor2 = random.randint(0, bg_img.size[1] - img.size[1])
        bg_img.paste(img, box=(anchor1, anchor2), mask=img)
    return bg_img


def generate(
        input_image_array: List['Image'],
        samples: int = 5,
        bg_img_path: Path = BACKGROUND_IMG_FOLDER / 'table1.jpg'
) -> None:
    for _ in tqdm(range(samples)):
        img_perm_lst = select_random_imgs(input_image_array)
        img = generate_image(img_perm_lst, bg_img_path=bg_img_path)
        img.save(OUTPUT_FOLDER / f"{dt.datetime.now()}.png")
