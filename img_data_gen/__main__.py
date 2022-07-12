from img_data_gen.generators import generate
from img_data_gen.loaders import load_all_images

input_img_array = load_all_images()
generate(input_img_array)
