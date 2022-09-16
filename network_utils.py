from ctypes import Array
from constants import FILE_BUFFER_SIZE, BYTE_MSG_DELIMITER, IMAGE_START
from byte_utils import string_from_bytes, to_bytes

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



def separate_instructions_from_bytes(bt: bytes) -> Array:
 
    i = 0
    while not __end_of_msg(chr(bt[i])):
        i += 1

    instruction = ""
    if i != 0:
        instruction = string_from_bytes(bt[:i])
    
    else:
        i = -1

    return [instruction, bt[i+1:]]


def __end_of_msg(char: str) -> bool:
  
    return char == BYTE_MSG_DELIMITER or char == IMAGE_START


def get_instruction_data(instructions: str) -> Array:
    instruction_data = instructions.split("|")
                
    num_of_bytes = int(instruction_data[2])
    image_id     = int(instruction_data[1])

    return [num_of_bytes, image_id]