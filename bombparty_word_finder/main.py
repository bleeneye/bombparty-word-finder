# BombParty Word Finder - A tool for automatic prompt completion in BombParty
# Copyright (C) 2025 BleenEye
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import platform
from typing import Any
from enum import Enum
from os import makedirs
from pathlib import Path
import json
from pynput import keyboard, mouse
from pynput.keyboard import Listener, Key, KeyCode
from pynput.mouse import Button
import pyperclip
import numpy as np
from numpy.typing import NDArray
import sys
import time
from .word_sorters import BaseSorter, make_sorter
from .vk_to_char import vk_to_char
from .wordlist import WORDLIST

sys.stdout.reconfigure(encoding="utf-8")


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


m_control = mouse.Controller()
kb_control = keyboard.Controller()
bombtext_loc = None
textbox_loc = None
chatbox_loc = None
cheat_enabled = False
n_words = 0
word_sorter = make_sorter("r")
reverse = False
previous_words = np.array([])
pressed_keys = set()
last_esc = 0


def decode_config() -> dict | None:
    if not CONFIG_DIR.is_dir():
        makedirs(CONFIG_DIR)
    if not CONFIG_FILE.is_file():
        print(f"No config file found at path {CONFIG_FILE}", flush=True)
        print("Created fresh config file\n", flush=True)
        save_params()
    with open(CONFIG_FILE, "r") as f:
        try:
            decoding = json.load(f)
        except:
            print(f"Error decoding config file at path {CONFIG_FILE}", flush=True)
            return None
    if not isinstance(decoding, dict):
        print(f"Error decoding config file at path {CONFIG_FILE}", flush=True)
        return None
    return decoding


def init_params() -> None:
    global bombtext_loc, textbox_loc, chatbox_loc, n_words, word_sorter, reverse
    params = decode_config()
    if params is None:
        print(f"Using basic defaults", flush=True)
        return
    set_bombtext_loc(params.get(ParamNames.BOMBTEXT_LOC.value))
    set_textbox_loc(params.get(ParamNames.TEXTBOX_LOC.value))
    set_chatbox_loc(params.get(ParamNames.CHATBOX_LOC.value))
    set_cheat_enabled(params.get(ParamNames.CHEAT_ENABLED.value))
    set_n_words(params.get(ParamNames.N_WORDS.value))
    set_reverse(params.get(ParamNames.REVERSE.value))
    word_sorter = make_sorter(params.get(ParamNames.WORD_SORTER_ID.value))


def save_params() -> None:
    if word_sorter is None:
        word_sorter_id = None
    else:
        word_sorter_id = word_sorter.id
    params = {
        ParamNames.BOMBTEXT_LOC.value: bombtext_loc,
        ParamNames.TEXTBOX_LOC.value: textbox_loc,
        ParamNames.CHATBOX_LOC.value: chatbox_loc,
        ParamNames.CHEAT_ENABLED.value: cheat_enabled,
        ParamNames.N_WORDS.value: n_words,
        ParamNames.WORD_SORTER_ID.value: word_sorter_id,
        ParamNames.REVERSE.value: reverse
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(params, f, indent=4)


def copy_bombtext() -> str | None:
    if bombtext_loc is None:
        print("WARNING: bombtext location has not been set", flush=True)
        return None
    m_control.position = (bombtext_loc[0], bombtext_loc[1])
    m_control.click(Button.left, 2)
    kb_control.press(CTRL_KEY)
    kb_control.press("c")
    kb_control.release(CTRL_KEY)
    kb_control.release("c")
    time.sleep(LAG_SLEEP)
    return pyperclip.paste().strip().lower()


def find_words(substring: str) -> NDArray:
    return WORDLIST[np.where(np.char.find(WORDLIST, substring) != -1)]


def paste_words(words: NDArray) -> None:
    if len(words) == 0:
        words = np.array(["null"])
    if cheat_enabled and textbox_loc is not None:
        m_control.position = (textbox_loc)
        m_control.click(Button.left)
        kb_control.type(words[0])
        kb_control.press(Key.enter)
        kb_control.release(Key.enter)
        words = np.delete(words, 0)
    if len(words) == 0:
        return
    time.sleep(LAG_SLEEP)
    if chatbox_loc is not None:
        m_control.position = (chatbox_loc)
        m_control.click(Button.left)
    pyperclip.copy(", ".join(words))
    kb_control.press(CTRL_KEY)
    kb_control.press("v")
    kb_control.release(CTRL_KEY)
    kb_control.release("v")
    time.sleep(LAG_SLEEP)
    kb_control.press(Key.enter)
    kb_control.release(Key.enter)
    if textbox_loc is not None:
        m_control.position = (textbox_loc)
        m_control.click(Button.left)


def autocomplete() -> None:
    global previous_words
    if bombtext_loc is None:
        print("WARNING: bombtext location not set. Skipping autocomplete...", flush=True)
        return
    substring = copy_bombtext()
    if substring is None:
        paste_words(np.zeros(0))
        return
    matching_words = find_words(substring)
    unused_matching_words = matching_words[~np.isin(matching_words, previous_words)]
    if word_sorter is None:
        sorted_words = unused_matching_words
    else:
        sorted_words = word_sorter.sort(unused_matching_words)
    if not reverse:
        selected_words = sorted_words[:n_words + 1]
    else:
        selected_words = sorted_words[:-1*(n_words + 2):-1]
    if len(selected_words) > 0:
        previous_words = np.append(previous_words, selected_words[0])
    paste_words(selected_words)


def format_point(point: Any) -> tuple[int, int] | None:
    if point is None:
        return None
    elif isinstance(point, tuple) and len(point) == 2 and all(isinstance(c, int) for c in point):
        return point
    elif isinstance(point, list) and len(point) == 2 and all(isinstance(c, int) for c in point):
        return tuple(point)
    else:
        raise ValueError(f"Could not format point {point}")


def set_bombtext_loc(loc: Any | None = None) -> None:
    global bombtext_loc
    bombtext_loc = format_point(loc)
    print(f"Bombtext location is {bombtext_loc}", flush=True)


def set_textbox_loc(loc: Any | None = None) -> None:
    global textbox_loc
    textbox_loc = format_point(loc)
    print(f"Textbox location is {textbox_loc}", flush=True)


def set_chatbox_loc(loc: Any | None = None) -> None:
    global chatbox_loc
    chatbox_loc = format_point(loc)
    print(f"Chatbox location is {chatbox_loc}", flush=True)


def set_cheat_enabled(enable: bool | None = None) -> None:
    global cheat_enabled
    if enable is None:
        cheat_enabled = False
    else:
        cheat_enabled = enable
    if cheat_enabled:
        print("Cheating is enabled", flush=True)
    else:
        print("Cheating is disabled", flush=True)


def set_n_words(n: int | None = None) -> None:
    global n_words
    if n is None:
        n_words = 0
    else:
        n_words = n
    print(f"Number of extra words is {n_words}", flush=True)


def set_reverse(state: bool | None = None) -> None:
    global reverse
    if state is None:
        reverse = False
    else:
        reverse = state
    if reverse:
        print("Sorting in reverse order", flush=True)
    else:
        print("Sorting in forward order", flush=True)


def on_press(key: Key | KeyCode | None) -> None:
    global word_sorter, pressed_keys, last_esc
    if key == Key.esc:
        if time.time() - last_esc < 0.5:
            save_params()
            return False
        last_esc = time.time()
        return
    pressed_keys.add(key)
    if key == Key.ctrl_l or key == Key.alt_l or key == Key.shift:
        return
    if key == Key.f4:
        autocomplete()
        return

    #ctrl + alt + shift commands
    if not {Key.ctrl_l, Key.alt_l, Key.shift} <= pressed_keys:
        return
    if isinstance(key, KeyCode):
        key_cha = vk_to_char(key.vk)
    else:
        return
    if key_cha is None:
        return
    if key_cha == "q":
        set_cheat_enabled(not cheat_enabled)
    elif key_cha == ".":
        set_bombtext_loc(m_control.position)
    elif key_cha == ",":
        set_textbox_loc(m_control.position)
    elif key_cha == "/":
        set_chatbox_loc(m_control.position)
    elif key_cha == "+":
        set_reverse(False)
    elif key_cha == "-":
        set_reverse(True)
    elif isinstance(key_cha, int):
        set_n_words(key_cha)
    elif isinstance(key_cha, str):
        new_sorter = make_sorter(key_cha)
        if new_sorter is None:
            return
        word_sorter = new_sorter
    save_params()


def on_release(key: Key| KeyCode | None) -> None:
    try:
        pressed_keys.remove(key)
    except KeyError:
        return


def display_preamble() -> None:
    print("""
##### YOU ARE USING THE BOMBPARTY WORD FINDER #####\n
    Use this while playing in a bomb party lobby to automatically fill in prompts.
    The tool also can post alternate solutions to each prompt in the chat.\n
    CONTROLS:
    ├── Quit: double tap esc (preferably not with terminal focused)
    ├── Autocomplete prompt: F4
    └── ALL CONTROLS BELOW USE <ctrl + alt + shift>
        ├── Set bombtext location (required): "."
        ├── Set textbox location (optional): ","
        ├── Set chatbox location (optional): "/"
        ├── Enable/Disable cheating: "q"
        ├── Set number of extra words to enter into chat: 0-9 (default 0)
        ├── Set sorting to forward: "+"
        ├── Set sorting to backward: "-"
        └── SET WORD SORTERS:""", flush=True)
    sorter_ids = BaseSorter.sorter_ids()
    for sorter_id, sorter_name in sorter_ids[:-1]:
        print(f"            ├── {sorter_name}: \"{sorter_id}\"", flush=True)
    print(f"            └── {sorter_ids[-1][1]}: \"{sorter_ids[-1][0]}\"\n", flush=True)


def main() -> None:
    display_preamble()
    init_params()
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    #kb_listener = Listener(on_press=on_press, on_release=on_release)
    #kb_listener.start()


if __name__ == "__main__":
    main()

