# git-annex gdrive special remote

__Work in progress, do not use this yet__

This wrapper around [gdrive](https://github.com/prasmussen/gdrive) based on [git-annex-remote-rclone](https://github.com/DanielDent/git-annex-remote-rclone) by Daniel Dent aims to add direct support for Google Drive to bypass some very annoying speed issues I was having with Google Drive via rclone.

## Installation

   1. [Install git-annex](https://git-annex.branchable.com/install/)
   2. [Install gdrive](https://github.com/prasmussen/gdrive) into your $PATH, e.g. `/usr/local/bin`
   3. Copy `git-annex-remote-gdrive` into your $PATH

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
