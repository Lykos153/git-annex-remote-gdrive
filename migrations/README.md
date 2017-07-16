# anything-to-nodir.py

__Still testing, use with care__

This script converts any folder structure on Google Drive to a `nodir` repository layout. It will recursively move all files in subdirectories to the top folder.

## Requirements
This scripts requires Python 3.6 and the libraries argparse and [pydrive](https://github.com/googledrive/PyDrive).

To install them via pip:

`pip install argparse PyDrive`

## Usage

```
anything-to-nodir.py [-h] [--token TOKEN] root

positional arguments:
  root           The root folder of the repository. Enter exactly what's
                 specified as 'prefix', by default that's 'git-annex'.

optional arguments:
  -h, --help     show this help message and exit
  --token TOKEN  If defined, access token will be stored in and loaded from
                 this file. By default, no credentials are stored.
```
As it's intended for single use it will not store your credentials by default. If you want to run it on multiple remotes or convert your remote in multiple steps, you can specify a file in which to store the access token. If the same file is specified again, the script will re-use the access token.

This example will make the folder /git-annex a `nodir` remote and store the access token in `token.json`

` ./anything-to-nodir.py git-annex --token token.json `

## Issues, Contributing

If you run into any problems, please check for issues on [GitHub](https://github.com/Lykos153/git-annex-remote-gdrive/issues).
Please submit a pull request or create a new issue for problems or potential improvements.

## License

Copyright 2017 Silvio Ankermann. Licensed under the GPLv3.
