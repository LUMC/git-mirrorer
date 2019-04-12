#!/usr/bin/env python3

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

import argparse
import os
import queue
import subprocess
import threading
from pathlib import Path
from typing import List, Tuple


class GitRepo(object):
    def __init__(self,
                 main_url: str,
                 mirror_urls: List[str],
                 repo_dir: Path):
        self.main_url = main_url
        self.mirror_urls = mirror_urls
        self.repo_dir = repo_dir

    def exists(self):
        return (self.repo_dir / Path(".git")).exists()

    def clone(self):
        if not self.exists():
            subprocess.run(args=["git", "clone", "--mirror", self.main_url,
                                 self.repo_dir.absolute()])

    def fetch(self):
        subprocess.run(args=["git", "-C", self.repo_dir.absolute(), "fetch"])

    def push_to_mirrors(self):
        for mirror_url in self.mirror_urls:
            subprocess.run(
                args=["git", "-C", self.repo_dir.absolute(), "push", "--all",
                      mirror_url])
            subprocess.run(
                args=["git", "-C", self.repo_dir.absolute(), "push", "--tags",
                      mirror_url])

    def mirror(self):
        """Mirrors the repo from the main git url to the miror git urls"""
        self.clone()
        self.fetch()
        self.push_to_mirrors()


class RepoQueue(queue.Queue):
    """A queue object that will hold git repos to be cloned and mirrored."""
    # Example taken from pytest-workflow's queue implementation.

    def __init__(self):
        # We will allow infinite sizes of queues
        super().__init__()
        # Allows is to store errors during processing
        self._process_errors = []

    def put(self, item, block=True, timeout=None):
        """Like Queue.put(item) but tests if item is a repo."""
        if isinstance(item, GitRepo):
            super().put(item, block, timeout)
        else:
            raise ValueError("Only GitRepo objects can be submitted to this "
                             "queue")

    def worker(self):
        """
        Clones repos until the queue is empty.
        """
        while True:
            try:
                # We know the type is GitRepo, because this was enforced in
                # the put method.
                repo = self.get_nowait()  # type: GitRepo
            except queue.Empty:
                break
            else:
                repo.mirror()
                self.task_done()

    def process(self, number_of_threads: int = 1):
        threads = []
        for _ in range(number_of_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)
        self.join()
        for thread in threads:
            thread.join()


def parse_config(config: Path) -> List[Tuple[str, List[str]]]:
    with config.open('rt') as config_h:
        config_lines = config_h.readlines()
    config_list = []
    for line in config_lines:
        clean_line = line.strip(os.linesep)
        source_url = clean_line.split('\t')[0]
        dest_urls = clean_line.split('\t')[1:]
        config_list.append((source_url, dest_urls))
    return config_list


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clone-dir", type=Path, dest="clone_dir",
                        help="Where repositories should be cloned on the "
                             "local machine.")
    parser.add_argument("--config", type=Path,
                        help="The configuration file")
    parser.add_argument("--threads", type=int,
                        help="how many git operations will be performed at the"
                             "same time.")
    return parser


def main():
    args = argument_parser().parse_args()
    clone_dir = args.clone_dir  # type: Path
    configuration = parse_config(args.config)  # type: List[Tuple[str, List[str]]]
    repo_queue = RepoQueue()
    for source_url, mirror_urls in configuration:
        git_repo = GitRepo(
            main_url=source_url,
            mirror_urls=mirror_urls,
            # Use the last part of the repo url to clone.
            # https://github.com/LUMC/git-synchronizer.git -> git-synchronizer.git
            repo_dir=clone_dir / Path(source_url.split('/')[-1])
        )
        repo_queue.put(git_repo)
    repo_queue.process()


if __name__ == "__main__":
    main()
