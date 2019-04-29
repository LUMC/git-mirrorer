.. git-synchronizer documentation master file, created by
   sphinx-quickstart on Mon Apr 29 08:25:29 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================
git-synchronizer
================

.. contents:: table of contents

============
Introduction
============

Git-synchronizer is an application meant to synchronize git repositories
with eachother. It can synchronize the main repository with one or more mirror
repositories.

Git-synchronizer fetches all branches and tags from the main repository and
pushes them to the mirror repositories.

Git-synchronizer is optimized to work in a cron job. Main and mirror repos are
set using a config file. Git-synchronizer supports fetching and pushing
multiple repositories at once.

============
Usage
============

.. argparse::
   :module: git_synchronizer.git_synchronizer
   :func: argument_parser
   :prog: git-synchronizer

Example config file
-------------------

::

   https://example.com/examples/example.git	git@mygit.com:/examples/example.git
   https://example.com/examples/example2.git	git@mygit.com:/examples/example2.git	git@myothergit.com/example/example2.git

