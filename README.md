# gitlab-dotenv
Synchronize Gitlab CI variables with a local file. Gitlab's interface is not perfect when one has to add/modify a lot of variables at once. This tool tries to solve this problem by providing a way to manage the variables locally and pushing the changed to Gitlab.

## Requirements
Should run on any Python 3.7+ installation with base packages available. The following imports are used: `argparse`, `configparser`, `copy`, `csv`, `os`, `pathlib`, `requests`, `urllib`.

## Usage
```
usage: gitlab-dotenv [-h] [-u URL] [-t TOKEN] [-m] [-d] [-a] [--remove] {push,pull} FILE

Synchronize Gitlab CI variables with a local file

positional arguments:
  {push,pull}         Action to perform
  FILE                CSV file to use as local storage

optional arguments:
  -h, --help          show this help message and exit
  -u URL              Gitlab project URL. If not provided the program tries to guess it using git remote "origin"
  -t TOKEN            Gitlab token with API rights. You can provide this in .gitlab-dotenv-token or ~/.config/gitlab-dotenv/token as well
  -m, --allow-modify  Modify existing variables if changed locally (push only)
  -d, --allow-delete  Delete variables if missing locally (push only)
  -a, --allow-all     Same as --allow-modify --allow-delete
  --remove            Remove every local variable from remote storage (push only)
```

### Examples
Read every CI variable from project `username/example-project` to `variables.csv`:
```
gitlab-dotenv -u 'https://gitlab.example.com/username/example-project' -t "${TOKEN}" pull variables.csv
```

Push every local change to project `username/example-project` from `variables.csv` including modifcations but do not delete variables that are not present locally:
```
gitlab-dotenv -u 'https://gitlab.example.com/username/example-project' -t "${TOKEN}" --allow-modify push variables.csv
```

The same command, but with the `TOKEN` stored in `.gitlab-dotenv-token` and with `git remote "origin"` set up:
```
gitlab-dotenv --allow-modify push variables.csv
```
