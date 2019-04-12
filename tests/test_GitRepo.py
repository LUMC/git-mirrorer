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

from git_synchronizer.git_synchronizer import GitRepo

import pytest


@pytest.fixture()
def git_repository():
    main_git = "https://github.com/LUMC/git-synchronizer.git"
    git_mirror_1 = str(Path(tempfile.mkdtemp(suffix=".git", prefix="mirror1")))
    git_mirror_2 = str(Path(tempfile.mkdtemp(suffix=".git", prefix="mirror2")))
    clone_dir = Path(str(tempfile.mkdtemp(prefix="clone_dir"))) / Path(
        "git-synchronizer.git")
    git_repo = GitRepo(main_url=main_git,
                       mirror_urls=[git_mirror_1, git_mirror_2],
                       repo_dir=clone_dir)
    return git_repo


def test_clone(git_repository):
    git_repo = git_repository
    assert not git_repo.repo_dir.exists()
    git_repo.clone()
    assert git_repo.repo_dir.exists()


