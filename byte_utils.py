from constants import DEFAULT_ENCODING

# Converter string para array de bytes
def to_bytes(text: str) -> bytes:
    return bytes(text,DEFAULT_ENCODING)

# Converter bytes para uma string
def string_from_bytes(bt: bytes) -> None:
    return str(bt,DEFAULT_ENCODING).strip()