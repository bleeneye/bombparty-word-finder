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


from shutil import rmtree
from .main import CONFIG_DIR


def main() -> None:
    answer = input("Delete all BombParty Word Finder configurations? ").lower()
    if answer != "y" and answer != "yes":
        quit()
    rmtree(CONFIG_DIR)
    print("Configuration files removed")

