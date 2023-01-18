import os.path

import slideio as slideio
from matplotlib import pyplot as plt

image_path = os.path.join('input', 'MD583.svs')
slide = slideio.open_slide(image_path, "SVS")
raw_string = slide.raw_metadata
print(raw_string.split("|"))

scene = slide.get_scene(0)
scene.name, scene.rect, scene.num_channels, scene.resolution

image = scene.read_block(size=(500, 0))
plt.imshow(image)
plt.show()

if __name__ == "__main__":
    pass
