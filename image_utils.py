from PIL import Image
import io

def open_image_as_byte_array(image_path: str) -> bytes:
  image = Image.open(image_path)
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, "PNG")
  imgByteArr.seek(0)
  imgByteArr = imgByteArr.read()

  return imgByteArr

def read_image_from_bytes(image_data) -> Image:
  image_bytes = io.BytesIO(image_data)
  return Image.open(image_bytes)