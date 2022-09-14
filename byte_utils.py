from multiprocessing.dummy import Array
from constants import DEFAULT_ENCODING

def to_bytes(text: str) -> bytes:
    return bytes(text.strip(),DEFAULT_ENCODING)

def string_from_bytes(bt: bytes) -> None:
    return str(bt,DEFAULT_ENCODING).strip()