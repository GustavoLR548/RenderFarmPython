from ctypes import Array
from constants import BYTE_MSG_DELIMITER, IMAGE_START, FILE_BUFFER_SIZE
from byte_utils import string_from_bytes, to_bytes

"""
A partir de um socket, e o numero de bytes da imagem,
fazer a captura continua dos pacotes de uma imagem, ate
que todos sejam recebidos
"""
def capture_image(conn, data, num_of_bytes):
        
        if not data:
            data = b''

        temp_data = conn.recv(FILE_BUFFER_SIZE)
        data      += temp_data 

        i = FILE_BUFFER_SIZE
        while i < num_of_bytes:
            temp_data  = conn.recv(FILE_BUFFER_SIZE)
            data      += temp_data 

            i += FILE_BUFFER_SIZE

        return data

# Fazer a mensagem de instrucao de envio adicionado o limitador
def to_image_instruction_msg(text: str) -> bytes:
  
    return to_bytes(text + BYTE_MSG_DELIMITER)

# Separar os bytes de instrucao dos bytes da mensagme
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


# Detectar fim da mensagem
def __end_of_msg(char: str) -> bool:
    return char == BYTE_MSG_DELIMITER or char == IMAGE_START


# Resgatar instrucoes de uma mensagem string
def get_instruction_data(instructions: str) -> Array:
    instruction_data = instructions.split("|")
                
    num_of_bytes = int(instruction_data[2])
    image_id     = int(instruction_data[1])

    return [num_of_bytes, image_id]