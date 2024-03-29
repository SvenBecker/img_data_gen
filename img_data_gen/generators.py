"""This module is actually responsible for generating randomized images."""
import datetime as dt
import functools
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List
import random
import json

import numpy as np
from tqdm import tqdm

from img_data_gen.constants import DEFAULT_NUM_WORKERS
from img_data_gen.loaders import ImageContainer, ImageLoader
from img_data_gen.transformers import ImageRotator

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

    def run(self, samples: int, draw_boxes: bool) -> None:
        """Generate images based on selected amount of `samples`."""
        with tqdm(total=samples) as pbar:
            with ThreadPoolExecutor(min(samples, DEFAULT_NUM_WORKERS)) as executor:
                # run image creation concurrently
                futures = [executor.submit(self.create_rnd_image, draw_boxes=draw_boxes) for _ in range(samples)]
                for _ in as_completed(futures):
                    # update the progressbar as soon as one of the images has been finished
                    pbar.update(1)
        
        self.save_labels([future.result() for future in futures])

    def create_rnd_image(self, draw_boxes: bool) -> Dict:
        """Create some randomized image file and save it."""

        # get a permutation of unique input images
        img_perm_map: Dict[str, 'Image'] = self.get_rnd_permutation()

        # select one background image at random
        bg_img: 'Image' = random.choice(self.image_container.bg_image_list)

        # create a new image as copy of the background image and a unique filename
        new_img = bg_img.copy()

        # Initialize image labels
        input_img_labels = []

        # paste input images into the new_img and randomly apply input image transformations
        for key, _img in img_perm_map.items():

            rotator = ImageRotator(_img)
            img, bbox = rotator.rnd_rotate()
            anchor1: int = random.randint(0, bg_img.size[0] - img.size[0])
            anchor2: int = random.randint(0, bg_img.size[1] - img.size[1])
            bbox = bbox.move(x=anchor1, y=anchor2)

            new_img.paste(img, box=(anchor1, anchor2), mask=img)
            if draw_boxes:
                bbox.draw(new_img)
            
            input_img_labels.append({
                'label': key,
                'bbox': bbox.vertices
            })

        # save image with unique filename
        base_filename = '-'.join(img_perm_map.keys())
        filename = f"{base_filename}-{dt.datetime.now().timestamp()}-{random.randrange(1, 10**4):04}.png"
        new_img.save(self.output_folder / filename)

        # cleanup
        new_img.close()
        del new_img

        #return entry to json file
        return(
            {
                'filename': filename,
                'input_images': input_img_labels
            }
        )

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

    def save_labels(self, entry: List[Dict]) -> None:
        """Saves labels consisting of image name, included card names, and bounding boxes to a file named 'labels.json' in the output folder"""

        json_fp = self.output_folder / 'labels.json'
        if not Path.is_file(json_fp):
            with open(json_fp,"w") as file:
                json.dump({'labels':[]}, file)

        with open(json_fp) as file:
            content = json.load(file)
        content['labels'].append(entry)

        with open(json_fp,'w') as file:
            json.dump(content, file, indent=2)