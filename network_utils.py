from constants import FILE_BUFFER_SIZE


def capture_image(socket,data,num_of_bytes):
    temp_data = socket.recv(FILE_BUFFER_SIZE)
    data      = temp_data 

    i = FILE_BUFFER_SIZE
    while i < num_of_bytes:
        temp_data  = socket.recv(FILE_BUFFER_SIZE)
        data      += temp_data 

        i += FILE_BUFFER_SIZE

    return data