RUNNING = True

DEBUG = True
DEBUG_PRINT_INFO_FREQUENCY = 180
tick_count = 0

# Framerate & display
FPS = 60
ROOT_SIZE = (300, 200)
SCALE = 3

def root_width() -> int:
    return ROOT_SIZE[0]
def root_height() -> int:
    return ROOT_SIZE[1]

def window_size() -> tuple[int, int]:
    return (ROOT_SIZE[0] * SCALE, ROOT_SIZE[1] * SCALE)
def window_width() -> int:
    return window_size()[0]
def window_height() -> int:
    return window_size()[1]

# Filepaths
LINGOJUNGLE_FP = "C:\\Users\\bdboo\\OneDrive\\Documents\\Programming Projects\\LingoJungle"
BIN_FP = f"{LINGOJUNGLE_FP}\\bin"
FONTS_FP= f"{BIN_FP}\\fonts"
TEXTURES_FP = f"{BIN_FP}\\textures"
AUDIO_FP = f"{BIN_FP}\\audio"
LESSONS_FP = f"{BIN_FP}\\lessons"
ICONS_FP = f"{TEXTURES_FP}\\icons"
USER_DATA_FP = f"{BIN_FP}\\user_data.json"