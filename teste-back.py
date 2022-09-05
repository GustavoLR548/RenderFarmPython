from email.errors import InvalidMultipartContentTransferEncodingDefect
from PIL import Image, ImageFilter
import numpy as np

# Splits an image into n_parts parts and returns an array
# containing each slab.
def split_img(img: Image, n_parts: int):
    
    slabs = {}
    # We need a counter to tell us where each slice is supposed to go when reconstructing the image
    counter = 0

    for i in range(n_parts):
        slabs[counter] = Image.fromarray(im[ i * int(len(im)/n_parts) : (i+1) * int(len(im)/n_parts) ] [0 : len(im[0])])
        counter += 1

    return slabs


# Merges all N slabs into a single image
def merge_img_slabs(slabs, n_parts):

    img = slabs[0]

    for i in range(1, n_parts):
        img = np.append(img, np.asarray(slabs[i]), axis=0)

    return Image.fromarray(img)


## SERVER
# Opens a image in RGB mode
im = Image.open(r"8k.jpg")

im = np.asarray(im)

# The number of slices that will come from an image. This is anologous to the number of
# clients connected to the server.
n_parts = 3

slabs = split_img(im, n_parts)

###

## CLIENT
# Blurring the image

# Cada cliente vai fazer o blur
for i in range(n_parts):
    slabs[i] = slabs[i].filter(ImageFilter.BoxBlur(20))

## Juntar as imagens de volta

reconstructed_img = merge_img_slabs(slabs, n_parts)
reconstructed_img.show()