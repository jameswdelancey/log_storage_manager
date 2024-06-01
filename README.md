# Log Storage Manager

## Overview

`log_storage_manager` is a Python script designed to manage log files by monitoring available disk space and deleting old log files when the free space falls below a specified threshold. It ensures that a minimum amount of free space is maintained on the disk to prevent log storage issues.

## Features

- **Automatic Log Management**: Monitors disk space and deletes old log files to maintain a specified amount of free space.
- **Flexible Configuration**: Allows customization of parameters such as the directory to monitor, minimum free space threshold, and sleep time between checks.
- **Debug Mode**: Enables verbose output for debugging purposes.
- **Dry Run Mode**: Simulates log file deletions without actually removing files, useful for testing and validation.

## Usage

```sh
python log_storage_manager.py --directory <directory_path> --min_gig_freespace <min_gig_freespace> --del_qty <del_qty> --log_id <log_id> [--debug] [--dry_run] [--sleep_time <sleep_time>] [--cache_file_path <cache_file_path>]
```

- `--directory`: Path to the directory to monitor for log files.
- `--min_gig_freespace`: Minimum amount of free space in gigabytes to maintain on the disk.
- `--del_qty`: Number of oldest log files to delete when free space is below the threshold.
- `--log_id`: Identifier to filter log files within the directory.
- `--debug` (optional): Enable debug mode for verbose output (default: disabled).
- `--dry_run` (optional): Simulate log file deletions without actually removing files (default: disabled).
- `--sleep_time` (optional): Time in seconds to sleep between disk space checks (default: 60 seconds).
- `--cache_file_path` (optional): Path to a cache file for storing processed log file paths (default: none).

## License

This Log Storage Manager script is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
