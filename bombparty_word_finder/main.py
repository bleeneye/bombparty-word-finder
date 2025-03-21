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


from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="BombParty Word Finder - A tool for automatic prompt completion in BombParty",
    )
    parser.add_argument(
        "-c",
        "--conditions",
        action="store_true",
        help="display conditions of redistribution"
    )
    parser.add_argument(
        "-w",
        "--warranty",
        action="store_true",
        help="display warranty disclaimer"
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="remove all BP Word Finder config files and directories"
    )
    return parser.parse_args()


def main() -> None:
    args = get_args()
    if args.uninstall:
        from . import uninstall
        uninstall.main()
        return
    if not args.conditions and not args.warranty:
        from . import bpfinder
        bpfinder.main()
        return
    from . import licensing
    if args.conditions:
        print(licensing.CONDITIONS)
    if args.warranty:
        print(licensing.WARRANTY)


if __name__ == "__main__":
    main()

