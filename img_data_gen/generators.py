"""This module is actually responsible for generating randomized images."""
import datetime as dt
import os
import functools
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Dict, cast
import random

import numpy as np
from tqdm import tqdm

from img_data_gen.loaders import ImageContainer, ImageLoader
from img_data_gen.transformers import rnd_transform

if TYPE_CHECKING:
    from PIL import Image


class ImageGenerator:
    """Generates images by merging one or more input images with some background image."""

    def __init__(self, input_img_folder: Path, bg_img_folder: Path, output_folder: Path):
        self.image_loader = ImageLoader(
            input_img_folder=input_img_folder,
            bg_img_folder=bg_img_folder
        )
        self.output_folder: Path = output_folder

    @functools.cached_property
    def image_container(self) -> ImageContainer:
        """Load input and background images and cache result."""
        return self.image_loader.load_all()

    def run(self, samples: int) -> None:
        """Generate images based on selected amount of `samples`."""
        with tqdm(total=samples) as pbar:
            with ThreadPoolExecutor(min(samples, cast(int, os.cpu_count()) + 4)) as executor:
                # run image creation concurrently
                futures = [executor.submit(self.create_rnd_image) for _ in range(samples)]
                for _ in as_completed(futures):
                    # update the progressbar as soon as one of the images has been finished
                    pbar.update(1)

    def create_rnd_image(self) -> None:
        """Create some randomized image file and save it."""

        # get a permutation of unique input images
        img_perm_map: Dict[str, 'Image'] = self.get_rnd_permutation()

        # select one background image at random
        bg_img: 'Image' = random.choice(self.image_container.bg_image_list)

        # create a new image as copy of the background image
        new_img = deepcopy(bg_img)

        # paste input images into the new_img and randomly apply input image transformations
        for _img in img_perm_map.values():
            img: 'Image' = rnd_transform(_img)   # todo: maybe change this
            anchor1: int = random.randint(0, bg_img.size[0] - img.size[0])
            anchor2: int = random.randint(0, bg_img.size[1] - img.size[1])
            new_img.paste(img, box=(anchor1, anchor2), mask=img)

        # save image as png
        filename = '-'.join(img_perm_map.keys())
        new_img.save(self.output_folder / f"{filename}-{dt.datetime.now().timestamp()}.png")

        # cleanup
        new_img.close()
        del new_img

    def get_rnd_permutation(self) -> Dict[str, 'Image']:
        """Get a random amount of input image names and Image objects and return it as a name - object mapping."""
        len_imgs = len(self.image_container.input_image_map)
        keys = list(self.image_container.input_image_map.keys())
        values = list(self.image_container.input_image_map.values())

        # get a random permutation of list indices
        idxs = np.random.permutation(np.arange(0, len_imgs))[0:random.randint(1, min(len_imgs, 9))]

        return {
            keys[idx]: values[idx]
            for idx in idxs
        }
