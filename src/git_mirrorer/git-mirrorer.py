#!/usr/bin/env python3

# git-mirrorer
# A program to mirror git repositories using cron.

# Copyright (C) 2019 Leiden University Medical Center
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import subprocess
from pathlib import Path


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clone-dir", type=Path, required=True,
                        help="Where repositories should be cloned on the "
                             "local machine.")
    parser.add_argument("--main-git-url")
    parser.add_argument("--mirror-git-url")
    return parser
