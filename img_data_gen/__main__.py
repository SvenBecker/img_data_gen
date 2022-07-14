"""This is the entrypoint of this package."""
import argparse
from pathlib import Path

from img_data_gen.constants import INPUT_IMG_FOLDER, BACKGROUND_IMG_FOLDER, OUTPUT_FOLDER
from img_data_gen.generators import ImageGenerator

parser = argparse.ArgumentParser(
    description="Run image data generation.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "-s", "--samples", type=int, default=10, help="The number of image samples to generate."
)
parser.add_argument(
    "-i", "--input-folder", type=Path, default=INPUT_IMG_FOLDER, help="Path to the input image folder."
)
parser.add_argument(
    "-b", "--bg-folder", type=Path, default=BACKGROUND_IMG_FOLDER, help="Path to the background image folder."
)
parser.add_argument(
    "-o", "--output-folder", type=Path, default=OUTPUT_FOLDER, help="Path to the output image folder."
)
args = parser.parse_args()

ImageGenerator(
    input_img_folder=args.input_folder,
    bg_img_folder=args.bg_folder,
    output_folder=args.output_folder
).run(samples=args.samples)
