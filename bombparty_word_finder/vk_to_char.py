# BombParty Word Finder
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


VK_TO_CHAR = {
    0x30: 0,
    0x31: 1,
    0x32: 2,
    0x33: 3,
    0x34: 4,
    0x35: 5,
    0x36: 6,
    0x37: 7,
    0x38: 8,
    0x39: 9,
    0x41: 'a',
    0x42: 'b',
    0x43: 'c',
    0x44: 'd',
    0x45: 'e',
    0x46: 'f',
    0x47: 'g',
    0x48: 'h',
    0x49: 'i',
    0x4a: 'j',
    0x4b: 'k',
    0x4c: 'l',
    0x4d: 'm',
    0x4e: 'n',
    0x4f: 'o',
    0x50: 'p',
    0x51: 'q',
    0x52: 'r',
    0x53: 's',
    0x54: 't',
    0x55: 'u',
    0x56: 'v',
    0x57: 'w',
    0x58: 'x',
    0x59: 'y',
    0x5a: 'z',
    0xBA: ';',      # Can vary per keyboard
    0xBB: '+',
    0xBC: ',',
    0xBD: '-',
    0xBE: '.',
    0xBF: '/',      # Can vary per keyboard
    0xC0: '`',      # Can vary per keyboard
    0xDB: '[',      # Can vary per keyboard
    0xDC: '\\',     # Can vary per keyboard
    0xDD: ']',      # Can vary per keyboard
    0xDE: '\'',     # Can vary per keyboard
}


def vk_to_char(vk: int) -> str | None:
    try:
        return VK_TO_CHAR[vk]
    except KeyError:
        return None

