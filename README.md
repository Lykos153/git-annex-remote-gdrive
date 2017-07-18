# git-annex gdrive special remote

This wrapper around [gdrive](https://github.com/prasmussen/gdrive) based on [git-annex-remote-rclone](https://github.com/DanielDent/git-annex-remote-rclone) aims to add direct support for Google Drive to git-annex. I forked it in order to bypass some very annoying performance issues I was having with Google Drive via rclone.

__Stability note:__
This has been forked from a quite stable application and been tested a lot during the last month. _Although it should be reliable, please for the time being keep additional copies of all data you do not want to lose._ A [numcopies](https://git-annex.branchable.com/git-annex-numcopies/) value greater than 1 is a good idea anyway.

## Requirements
The current version of git-annex-remote-gdrive has been tested with gdrive version 2.1.0. Gdrive may change its output in the future, so updates to this software may be required for compatibility.

To simplify maintenance, when I make updates to git-annex-remote-gdrive, I test only against the current stable
version of gdrive. While I am not currently explicitly dropping support for older versions, I am neither
performing additional integration tests with older gdrive versions.

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
git annex initremote google type=external externaltype=gdrive prefix=git-annex chunk=50MiB encryption=shared mac=HMACSHA512
```
The initremote command calls out to GPG and can hang if a machine has insufficient entropy. To debug issues, use the `--debug` flag, i.e. `git-annex initremote --debug`.

## Using an existing remote (note on repository layout)

If you're switching from git-annex-remote-rclone, it's as simple as typing `git annex enableremote <remote_name> externaltype=gdrive`. git-annex-remote-gdrive supports all repository layouts currently supported by git-annex-remote-rclone and will automatically import its options if nothing is specified. You can explicitely specify the layout with the option `gdrive_layout` (which works on `initremote` and `enableremote`). You can keep your repository layout if you want. Even with a two-level hierarchy, gdrive is still significantly faster than rclone on Google Drive (~factor 3).  But you might want to consider [migrating](https://github.com/Lykos153/git-annex-remote-gdrive/tree/master/migrations) the layout to `nodir` to get the best performance.

Google Drive requires us to traverse the whole path on each file operation, which results in a noticeable performance loss (especially during upload). On the other hand, it's perfectly fine to have thousands of files in one Google Drive folder as it doesn't event use a folder structure internally. So the best option for special remotes on GD is the `nodir` layout.

The following layouts are currently supported:
 * `nodir` - No directory hierarchy is used.
    * This is the simplest and most efficient layout for Google Drive. New repos should always use is.
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
