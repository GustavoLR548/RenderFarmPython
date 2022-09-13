from PIL import Image, ImageFilter
import numpy as np


# Adds <blur_radius> pixels to the TOP of the image. 
def add_top_pixels(original_img, slab, slab_number: int, blur_radius: int, n_parts: int):
    temp = original_img[(slab_number * int(len(original_img)/n_parts) - blur_radius) : (slab_number * int(len(original_img)/n_parts))][0 : len(original_img[0])]
    slab = np.append(temp, slab, axis=0)

    return slab


# Adds <blur_radius> pixels to the BOTTOM of the image.
def add_bottom_pixels(original_img, slab, slab_number: int, blur_radius: int, n_parts: int):
    temp = original_img[((slab_number+1) * int(len(original_img)/n_parts)) : ((slab_number+1) * int(len(original_img)/n_parts)) + blur_radius][0 : len(original_img[0])]
    slab = np.append(slab, temp, axis=0)

    return slab


# Removes <blur_radius> pixels from the TOP of the image.
def remove_top_pixels(slab, blur_radius: int):
    slab = slab[ blur_radius : len(slab)][0 : len(slab[0])]

    return slab


# Removes <blur_radius> pixels from the BOTTOM of the image.
def remove_bottom_pixels(slab, blur_radius: int):
    slab = slab[ 0 : len(slab) - blur_radius][0 : len(slab[0])]

    return slab


# Splits an image into n_parts parts and returns an array
# containing each slab.
def split_img(original_img, n_parts: int, blur_radius: int) -> dict:
    
    slabs = {}
    # We need a counter to tell us where each slice is supposed to go when reconstructing the image
    counter = 0

    for i in range(n_parts):
        temp_slab = (original_img[ i * int(len(original_img)/n_parts) : (i+1) * int(len(original_img)/n_parts) ] [0 : len(original_img[0])])
        
        if counter != 0:
            temp_slab = add_top_pixels(original_img, temp_slab, counter, blur_radius, n_parts)

        if counter != (n_parts-1):
            temp_slab = add_bottom_pixels(original_img, temp_slab, counter, blur_radius, n_parts)

        slabs[counter] = Image.fromarray(temp_slab)
        counter += 1

    return slabs


# Merges all N slabs into a single image
def merge_img_slabs(slabs, n_parts: int, blur_radius: int) -> Image:

    img = slabs[0]
    img = remove_bottom_pixels(np.asarray(img), blur_radius)
    
    for i in range(1, n_parts):
        
        temp_slab = np.asarray(slabs[i])

        if i != (n_parts-1):
            temp_slab = remove_bottom_pixels(temp_slab, blur_radius)

        temp_slab = remove_top_pixels(temp_slab, blur_radius)

        img = np.append(img, temp_slab, axis=0)

    return Image.fromarray(img)


## SERVER
# Opens a image in RGB mode
original_image = Image.open(r"8k.jpg")

original_image = np.asarray(original_image)

# The number of slices that will come from an image. This is anologous to the number of
# clients connected to the server.
N_SLABS = 4
BLUR_RADIUS = 5

slabs = split_img(original_image, N_SLABS, BLUR_RADIUS)

print(type(slabs[0]))
## CLIENT
# Blurring the image

for i in range(N_SLABS):
    slabs[i] = slabs[i].filter(ImageFilter.BoxBlur(BLUR_RADIUS))


## SERVER
# Reconstruct the image
reconstructed_img = merge_img_slabs(slabs, N_SLABS, BLUR_RADIUS)
reconstructed_img.show()