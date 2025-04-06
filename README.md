# Folder Sync Tool

A simple Python program for one-way folder synchronization.

## Features

- Keeps the replica folder identical to the source folder
- Runs periodically at a specified interval
- Compares file contents using MD5 hashes
- Logs all operations to both console and file
- Does not use any external sync libraries

## Usage

```bash
python sync_tool.py <source_path> <replica_path> <interval_seconds> <log_file_path>
```

Example:

```bash
python sync_tool.py ./source ./replica 60 sync.log
```

## Tests

To run the integration test:

```bash
python integration_test.py
```

## Requirements

- Python 3.6 or higher
- No third-party dependencies
