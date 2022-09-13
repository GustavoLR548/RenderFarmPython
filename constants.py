# Socket constants
FILE_BUFFER_SIZE = 4096
MSG_BUFFER_SIZE  = 1024

# Socket communication constants
SENDING_IMAGE = "SENDING_IMAGE"

# Reserved words for messaging
RESERVED_MESSAGES = [
    "!quit",
    "!help"
]

QUIT_PROGRAM = RESERVED_MESSAGES[0]

# Connection constants
LOCALHOST    = "127.0.0.1"
DEFAULT_PORT = 5000
LOCAL_CONNECTION = (LOCALHOST,DEFAULT_PORT)

# Character encoding constants
DEFAULT_ENCODING = "utf-8"