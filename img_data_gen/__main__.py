import time
from img_data_gen.generators import ImageGenerator
from img_data_gen.loaders import ImageLoader

start = time.time()
img_container = ImageLoader().load_all()
ImageGenerator(input_image_mapping=img_container.input_image_map, background_image_array=img_container.bg_image_list).run(samples=20)
print(f'Run took {time.time() - start} seconds.')

