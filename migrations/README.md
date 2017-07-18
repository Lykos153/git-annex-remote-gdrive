# anything-to-nodir.py

__Still testing, use with care__

This script converts any folder structure on Google Drive to a `nodir` repository layout. It will recursively move all files in subdirectories to the top folder.

## Requirements
This scripts requires Python 3.6 and the libraries argparse, [pydrive](https://github.com/googledrive/PyDrive) and [tenacity](https://github.com/jd/tenacity).

To install them via pip:

`pip install argparse PyDrive tenacity`

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

## Keep using remote while migrating

During the migration process, the special remote is in an undefined state. Some of the files you want to access might not be in the expected place. Normally, git-annex-remote-gdrive will traverse the whole path to the file and only respect files that are in the right place. However, it can be told to be a bit more relaxed about from where to read a file. It will then look for the filename in the whole Drive whithout restriction to a specific parent folder. Due to git-annex's [cryptographic key values](http://git-annex.branchable.com/backends/), there is no danger of reading the wrong content.

This option does not affect file upload and deletion. Even in relaxed mode, git-annex-remote-gdrive will always put files into and delete files from the folder determined by the specified layout, so there's no danger of data loss either.

To use the remote while migrating:

1. `git annex enableremote <remotename> gdrive_layout=nodir traverse=relaxed` - This will put new uploaded files into the right folder but allows to read the files which are not yet migrated
2. `anything-to-nodir.py <remote root>` - Run the migration
3. `git annex enableremote <remotename> traverse=strict` - Revert to strict mode. git-annex-remote-gdrive will work only work on the `nodir` layout

## Running the script on a headless server

You can use the `--token` option for this. 

1. Run `./anything-to-nodir.py somefolder --token token.json` on your workstation and abort after authenticating
2. Transfer `token.json` to the server
2. Run `./anything-to-nodir.py <remote root> --token token.json`

## Issues, Contributing

The migration is not very fast (~5 minutes / 100 files). PyDrive [still uses Google's API v2](https://github.com/googledrive/PyDrive/issues/99#issuecomment-314091631), maybe that's why - maybe not. Fortunately it has to be done only once and we can keep using the repo meanwhile.

If you run into any problems, please check for issues on [GitHub](https://github.com/Lykos153/git-annex-remote-gdrive/issues).
Please submit a pull request or create a new issue for problems or potential improvements.

## License

Copyright 2017 Silvio Ankermann. Licensed under the GPLv3.
