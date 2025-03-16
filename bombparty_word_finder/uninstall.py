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
    if not CONFIG_DIR.is_dir():
        print("No configuration exists")
        return
    answer = input("Delete all BombParty Word Finder configurations? (y/n) ").lower()
    if answer == "y" or answer == "yes":
        rmtree(CONFIG_DIR)
        print("Configuration files removed")
    elif answer == "n" or answer == "no":
        print("Quitting - Configuration files not removed")
    else:
        print("Please enter \"y\", \"yes\", \"n\", or \"no\" (case insensitive)")
        main()

