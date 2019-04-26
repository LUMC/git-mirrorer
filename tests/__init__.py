# Copyright (C) 2019 Leiden University Medical Center
# This file is part of git-synchronizer
#
# git-synchronizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# git-synchronizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with git-synchronizer.  If not, see <https://www.gnu.org/licenses/

import tempfile
from pathlib import Path

import git


def clone_this_repo() -> git.Repo:
    this_repo = Path(__file__).parent.parent
    return git.Repo.clone_from(str(this_repo), Path(
        tempfile.mkdtemp(suffix=".git", prefix="origin")).absolute())


def empty_repo() -> git.Repo:
    temp_dir = Path(
        tempfile.mkdtemp(suffix=".git", prefix="mirror1")).absolute()
    repo = git.Repo.init(str(temp_dir))
    return repo
