from ctypes import Array
from constants import FILE_BUFFER_SIZE, BYTE_MSG_DELIMITER, IMAGE_START
from byte_utils import to_bytes

def capture_image(socket,data,num_of_bytes):

    if not data:
        data = b''

    temp_data = socket.recv(FILE_BUFFER_SIZE)
    data      += temp_data 

    i = FILE_BUFFER_SIZE
    while i < num_of_bytes:
        temp_data  = socket.recv(FILE_BUFFER_SIZE)
        data      += temp_data 

        i += FILE_BUFFER_SIZE

    return data


def to_image_instruction_msg(text: str) -> bytes:
    return to_bytes(text + BYTE_MSG_DELIMITER)


def extract_instruction_from_bytes(bt: bytes) -> Array:
    instruction: str = ""
    i = 0
    for i in range(len(bt)):
        char = chr(bt[i])

        if char == BYTE_MSG_DELIMITER or char == IMAGE_START:
            break
        instruction += char

    return [instruction, bt[i+1:]]
