import random
from typing import List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from PIL import Image


def select_random_imgs(img_lst: List['Image']) -> List['Image']:
    len_imgs = len(img_lst)
    idxs = np.random.permutation(np.arange(0, len_imgs))[0:random.randint(1, min(len_imgs, 9))]
    return [
        img_lst[idx]
        for idx in idxs
    ]
