"""Contains certain constants."""
import os
from pathlib import Path

ROOT_FOLDER = Path(__file__).parents[1]
BACKGROUND_IMG_FOLDER = ROOT_FOLDER / 'data' / 'background'
INPUT_IMG_FOLDER = ROOT_FOLDER / 'data' / 'input'
OUTPUT_FOLDER = ROOT_FOLDER / 'output'

DEFAULT_NUM_WORKERS: int = (os.cpu_count() or 28) + 4
