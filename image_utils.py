from typing import overload
from PIL import Image, ImageFilter
from io import BytesIO

import numpy as np

@overload(str)
def open_image_as_byte_array(img_path: str) -> bytes:
  
  img = Image.open(img_path)
  return open_image_as_byte_array(img)


@overload(Image)
def open_image_as_byte_array(img: Image) -> bytes:
  imgByteArr = BytesIO()
  img.save(imgByteArr, "PNG")
  
  imgByteArr.seek(0)
  imgByteArr = imgByteArr.read()

  return imgByteArr

def open_image_as_numpy_array(img_path: str):
  
  original_image = Image.open(img_path)
  original_image = np.asarray(original_image)

  return original_image

def read_image_from_bytes(image_data) -> Image:

  image_bytes = BytesIO(image_data)
  return Image.open(image_bytes)


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

def apply_blur(image: Image, blur_radius: float):
    return image.filter(ImageFilter.BoxBlur(blur_radius))


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