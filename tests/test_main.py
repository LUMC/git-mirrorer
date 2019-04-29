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

import sys
import tempfile
import textwrap
from pathlib import Path

import git

from git_synchronizer.git_synchronizer import main

from . import clone_this_repo, empty_repo


def config_file() -> Path:
    config = textwrap.dedent("""\
    {main_repo}\t{mirror_one}\t{mirror_two}
    """.format(
        main_repo=clone_this_repo().working_dir,
        mirror_one=empty_repo().working_dir,
        mirror_two=empty_repo().working_dir
    ))
    _, temp_file = tempfile.mkstemp(prefix="config", suffix=".tsv")
    temp_path = Path(str(temp_file))
    with temp_path.open('wt') as handler:
        handler.write(config)
    return temp_path


def test_main():
    clone_dir = Path(str(tempfile.mkdtemp(prefix="clonedir")))
    config = config_file()
    with config.open('rt') as config_h:
        config_lines = config_h.readlines()
    origin, mirror_one, mirror_two = config_lines[0].strip('\n').split('\t')[:]
    # [7:] removes the "file://" bit.
    one = git.Repo(mirror_one)
    two = git.Repo(mirror_two)
    assert len(one.branches) == 0
    assert len(two.branches) == 0
    sys.argv = [
        "git-synchronizer",
        "--clone-dir", str(clone_dir),
        "--config", str(config),
    ]
    main()
    cloned_repo = clone_dir / Path(origin.split('/')[-1])
    repo_clone = git.Repo(cloned_repo)
    assert clone_dir.exists()
    assert cloned_repo.exists()
    assert repo_clone.bare
    assert len(one.branches) > 0
    assert len(two.branches) > 0
