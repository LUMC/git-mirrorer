# git-synchronizer

Git-synchronizer is an application meant to synchronize git repositories with eachother. It can synchronize the main repository with one or more mirror repositories.

Git-synchronizer fetches all branches and tags from the main repository and pushes them to the mirror repositories.

Git-synchronizer is optimized to work in a cron job. Main and mirror repo’s are set using a config file. Git-synchronizer supports fetching and pushing multiple repositories at once.

For more information checkout our [readthedocs page](https://git-synchronizer.readthedocs.io/).

