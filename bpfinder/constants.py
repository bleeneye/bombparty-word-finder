import platform
from enum import Enum
from pathlib import Path
from pynput.keyboard import Key


class ParamNames(Enum):
    BOMBTEXT_LOC = "bombtext_loc"
    TEXTBOX_LOC = "textbox_loc"
    CHATBOX_LOC = "chatbox_loc"
    CHEAT_ENABLED = "cheat_enabled"
    N_WORDS = "n_words"
    WORD_SORTER_ID = "word_sorter_id"
    REVERSE = "reverse"


CONFIG_DIR = Path.home().joinpath(".config/bombparty_word_finder")
CONFIG_FILE = CONFIG_DIR.joinpath("config.json")
LAG_SLEEP = 0.02
if platform.system() == "Darwin":
    CTRL_KEY = Key.cmd
else:
    CTRL_KEY = Key.ctrl

