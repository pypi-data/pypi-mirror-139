# Unifi Protect Backup


[![pypi](https://img.shields.io/pypi/v/unifi-protect-backup.svg)](https://pypi.org/project/unifi-protect-backup/)
[![python](https://img.shields.io/pypi/pyversions/unifi-protect-backup.svg)](https://pypi.org/project/unifi-protect-backup/)
[![Build Status](https://github.com/ep1cman/unifi-protect-backup/actions/workflows/dev.yml/badge.svg)](https://github.com/ep1cman/unifi-protect-backup/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/ep1cman/unifi-protect-backup/branch/main/graphs/badge.svg)](https://codecov.io/github/ep1cman/unifi-protect-backup)

A Python based tool for backing up Unifi Protect event clips as they occur.

* GitHub: <https://github.com/ep1cman/unifi-protect-backup>
* PyPI: <https://pypi.org/project/unifi-protect-backup/>
* Free software: MIT

[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/ep1cman)

## Features

- Listens to events in real-time via the Unifi Protect websocket API
- Supports uploading to a [wide range of storage systems using `rclone`](https://rclone.org/overview/)
- Performs nightly pruning of old clips

## Requirements
- Python 3.9+
- Unifi Protect version 1.20 or higher (as per [`pyunifiproect`](https://github.com/briis/pyunifiprotect))
- `rclone` installed with at least one remote configured.

## Installation

1. Install `rclone.` Instructions for your platform can be found here: https://rclone.org/install/#quickstart
2. Configure the `rclone` remote you want to back to. Instructions can be found here: https://rclone.org/docs/#configure
3. `pip install unifi-protect-backup`

## Usage
```
Usage: unifi-protect-backup [OPTIONS]

  A Python based tool for backing up Unifi Protect event clips as they occur.

Options:
  --address TEXT                  Address of Unifi Protect instance
                                  [required]
  --port INTEGER                  Port of Unifi Protect instance
  --username TEXT                 Username to login to Unifi Protect instance
                                  [required]
  --password TEXT                 Password for Unifi Protect user  [required]
  --verify-ssl / --no-verify-ssl  Set if you do not have a valid HTTPS
                                  Certificate for your instance
  --rclone-destination TEXT       `rclone` destination path in the format
                                  {rclone remote}:{path on remote}. E.g.
                                  `gdrive:/backups/unifi_protect`  [required]
  --retention TEXT                How long should event clips be backed up
                                  for. Format as per the `--max-age` argument
                                  of rclone`
                                  (https://rclone.org/filtering/#max-age-don-
                                  t-transfer-any-file-older-than-this)
  -v, --verbose                   How verbose the logging output should be.

                                  None: Only log info messages created by
                                  `unifi-protect-backup`, and all warnings

                                  -v: Only log info & debug messages created
                                  by `unifi-protect-backup`, and all warnings

                                  -vv: Log info & debug messages created by
                                  `unifi-protect-backup`, command output, and
                                  all warnings

                                  -vvv Log debug messages created by `unifi-
                                  protect-backup`, command output, all info
                                  messages, and all warnings

                                  -vvvv: Log debug messages created by `unifi-
                                  protect-backup` command output, all info
                                  messages, all warnings, and websocket data

                                  -vvvvv: Log websocket data, command output,
                                  all debug messages, all info messages and
                                  all warnings  [x>=0]
  --help                          Show this message and exit.
```

The following environment variables can also be used instead of command line arguments (note, CLI arguments
always take priority over environment variables):
- `UFP_USERNAME`
- `UFP_PASSWORD`
- `UFP_ADDRESS`
- `UFP_PORT`
- `UFP_SSL_VERIFY`
- `RCLONE_RETENTION`
- `RCLONE_DESTINATION`

## Credits

Heavily utilises [`pyunifiproect`](https://github.com/briis/pyunifiprotect) by [@briis](https://github.com/briis/)


This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.
