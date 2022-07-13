import datetime as dt
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
import random

import numpy as np
from tqdm import tqdm
from PIL import Image

from img_data_gen.constants import OUTPUT_FOLDER
from img_data_gen.transformers import rnd_transform


@dataclass
class ImageGenerator:
    input_image_mapping: Dict[str, 'Image']
    bg_image_list: List['Image']
    output_folder: Path = OUTPUT_FOLDER

    def run(self, samples: int = 10) -> None:
        with tqdm(total=samples) as pbar:
            with ThreadPoolExecutor(min(samples, os.cpu_count() + 4)) as executor:
                # run image creation concurrently
                futures = [executor.submit(self.create_rnd_image) for _ in range(samples)]
                for _ in as_completed(futures):
                    # update the progressbar as soon as one of the images has been finished
                    pbar.update(1)

    def create_rnd_image(self) -> None:
        # get a permutation of unique input images
        img_perm_map: Dict[str, 'Image'] = self.get_rnd_permutation()

        # select one background image at random
        bg_img: 'Image' = random.choice(self.bg_image_list)

        # create a new image as copy of the background image
        new_img = deepcopy(bg_img)

        # paste input images into the new_img and randomly apply input image transformations
        for img in img_perm_map.values():
            img: 'Image' = rnd_transform(img)   # todo: maybe change this
            anchor1: int = random.randint(0, bg_img.size[0] - img.size[0])
            anchor2: int = random.randint(0, bg_img.size[1] - img.size[1])
            new_img.paste(img, box=(anchor1, anchor2), mask=img)

        # save image as png
        filename = '-'.join(img_perm_map.keys())
        new_img.save(OUTPUT_FOLDER / f"{filename}-{dt.datetime.now().timestamp()}.png")

        # cleanup
        new_img.close()
        del new_img

    def get_rnd_permutation(self) -> Dict[str, 'Image']:
        len_imgs = len(self.input_image_mapping)
        keys = list(self.input_image_mapping.keys())
        values = list(self.input_image_mapping.values())

        # get a random permutation of list indices
        idxs = np.random.permutation(np.arange(0, len_imgs))[0:random.randint(1, min(len_imgs, 9))]

        return {
            keys[idx]: values[idx]
            for idx in idxs
        }
