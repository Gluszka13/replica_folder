import os
import shutil
import time
import argparse
import logging
import hashlib

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_file(src, dst):
    shutil.copy2(src, dst)
    logging.info(f"Copied file: {src} -> {dst}")

def delete_file(path):
    os.remove(path)
    logging.info(f"Deleted file: {path}")

def delete_dir(path):
    shutil.rmtree(path)
    logging.info(f"Deleted folder: {path}")

def create_missing_dirs(source, replica):
    for root, dirs, _ in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)
        for dir_name in dirs:
            dir_path = os.path.join(replica_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"Created folder: {dir_path}")

def sync_files(source, replica):
    for root, _, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)
        for file_name in files:
            src_file = os.path.join(root, file_name)
            replica_file = os.path.join(replica_root, file_name)
            if not os.path.exists(replica_file):
                copy_file(src_file, replica_file)
            else:
                if calculate_md5(src_file) != calculate_md5(replica_file):
                    copy_file(src_file, replica_file)

def remove_extra_items(source, replica):
    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, rel_path)
        for file_name in files:
            replica_file = os.path.join(root, file_name)
            src_file = os.path.join(source_root, file_name)
            if not os.path.exists(src_file):
                delete_file(replica_file)
        for dir_name in dirs:
            replica_dir = os.path.join(root, dir_name)
            src_dir = os.path.join(source_root, dir_name)
            if not os.path.exists(src_dir):
                delete_dir(replica_dir)

def sync_dirs(source, replica):
    if not os.path.exists(replica):
        os.makedirs(replica)
    create_missing_dirs(source, replica)
    sync_files(source, replica)
    remove_extra_items(source, replica)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('replica')
    parser.add_argument('interval', type=int)
    parser.add_argument('log_file')
    args = parser.parse_args()

    setup_logging(args.log_file)

    while True:
        sync_dirs(args.source, args.replica)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
