# git-annex gdrive special remote

__Still testing, use with care__

This wrapper around [gdrive](https://github.com/prasmussen/gdrive) based on [git-annex-remote-rclone](https://github.com/DanielDent/git-annex-remote-rclone) by Daniel Dent aims to add direct support for Google Drive to bypass some very annoying speed issues I was having with Google Drive via rclone.

## Requirements
The current version of git-annex-remote-gdrive has been tested with gdrive version 2.1.0. Gdrive may change its output in the future, so updates to this software may be required for compatibility.

To simplify maintenace, when I make updates to git-annex-remote-rclone, I test only against the current stable
version of rclone. While I am not currently explicitly dropping support for older versions, I am also not
performing additional integration tests with older rclone versions.

## Installation

   1. [Install git-annex](https://git-annex.branchable.com/install/)
   2. [Install gdrive](https://github.com/prasmussen/gdrive) into your $PATH, e.g. `/usr/local/bin`
   3. Copy `git-annex-remote-gdrive` into your $PATH

## Usage

1. To create a gdrive config file, just use any gdrive command: eg. `gdrive about`
2. Create a git-annex repository ([walkthrough](https://git-annex.branchable.com/walkthrough/))
3. Add a remote for Google Drive. This example:

   * Adds a git-annex remote called `google`
   * Uses 50MiB chunks
   * Encrypts all chunks prior to uploading and stores the key within the annex repository
   * Uses a `nodir` repository layout
   * Stores your files in a folder/prefix called `git-annex`:

```
git annex initremote google type=external externaltype=gdrive prefix=git-annex chunk=50MiB encryption=shared mac=HMACSHA512 gdrive_layout=nodir
```
The initremote command calls out to GPG and can hang if a machine has insufficient entropy. To debug issues, use the `--debug` flag, i.e. `git-annex initremote --debug`.

## Using an existing remote (note on repository layout)

git-annex-remote-gdrive supports all repository layouts currently supported by git-annex-remote-rclone. You can specify the layout with the option `gdrive_layout` on `initremote` or `enableremote`. That being said, there is no reason to use a layout other than `nodir` on a new remote. Google Drive requires us to traverse the whole path on each file operation, which results in a noticeable performance loss (especially during upload). On the other hand, it's perfectly fine to have thousands of files in one Google Drive folder as it doesn't event use a folder structure internally. So the best option for special remotes on GD is the `nodir` layout.

If you're switching from rclone to gdrive for your special repo and you want to keep your layout, that's fine. Gdrive is still significantly faster than rclone on Google Drive.  But you might want to consider migrating the layout to `nodir` to get the best performance.

The following layouts are currently supported:
 * `nodir` - No directory hierarchy is used.
    * This is the simplest and most efficient layout for Google Drive.
 * `lower` - A two-level lower case directory hierarchy is used (using git-annex's DIRHASH-LOWER MD5-based format). This choice requires git-annex 6.20160511 or later.
 * `directory` - A two-level lower case directory hierarchy is used, along with the key name as a 3rd level nested directory. This choice requires git-annex 6.20160511 or later.
 * `mixed` - A two-level mixed case directory hierarchy is used (using git-annex's DIRHASH format).
 * `frankencase` - A two-level lower case directory hierarchy is used (using git-annex's DIRHASH format, with all characters translated to lower case)
    * This layout should not be used except if you already have a legacy remote using this layout and do not wish to migrate.
    * This was the only available layout in early versions of git-annex-remote-rclone, up to release v0.1.

## Choosing a Chunk Size

Choose your chunk size based on your needs. By using a chunk size below the maximum file size supported by
your cloud storage provider for uploads and downloads, you won't need to worry about running into issues with file size.
Smaller chunk sizes: leak less information about the size of file size of files in your repository, require less ram,
and require less data to be re-transmitted when network connectivity is interrupted. Larger chunks require less round
trips to and from your cloud provider and may be faster. Additional discussion about chunk size can be found
[here](https://git-annex.branchable.com/chunking/) and [here](https://github.com/DanielDent/git-annex-remote-rclone/issues/1)

## Implementation Note

At this time, this remote does NOT store your credentials in git-annex. Users are responsible for ensuring a
config file with valid credentials is available.

## Issues, Contributing

If you run into any problems, please check for issues on [GitHub](https://github.com/Lykos153/git-annex-remote-gdrive/issues).
Please submit a pull request or create a new issue for problems or potential improvements.

## License

Copyright 2017 Silvio Ankermann. Licensed under the GPLv3.
