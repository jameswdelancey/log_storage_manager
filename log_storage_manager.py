# Copyright 2022 James Delancey
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import sys
import shutil
import os
import time

BYTES_PER_GIG = 1024 * 1024 * 1024

directory = ""
min_gig_freespace = 10
sleep_time = 60
current_free_space = 10
del_qty = 10
cache_file_path = ""
log_id = ""
cache = []
next_del_batch = []
debug = False
dry_run = False


def check_freespace():
    global directory, current_free_space, debug
    if debug:
        print("checking freespace", file=sys.stderr, flush=True)
    total, used, free = shutil.disk_usage(directory)
    current_free_space = free // BYTES_PER_GIG
    if debug:
        print(
            f"current free space is: {current_free_space}", file=sys.stderr, flush=True
        )


def check_filelist():
    global directory, cache_file_path, log_id, cache, next_del_batch, debug, dry_run

    if len(cache) < del_qty:
        if cache_file_path and os.path.isfile(cache_file_path):
            if debug:
                print(
                    f"reading cache file: {cache_file_path}",
                    file=sys.stderr,
                    flush=True,
                )
            with open(cache_file_path) as f:
                cache.extend(f.read().splitlines())

    # we have filled cache from cache_file_path, unsorted
    if len(cache) < del_qty:
        if debug:
            print("getting list of files from dir", file=sys.stderr, flush=True)
        cache.extend([os.path.join(directory, x) for x in os.listdir(directory)])
    # we have filled cache from directory, unsorted
    if debug:
        print(f"cache length is: {len(cache)}", file=sys.stderr, flush=True)
    for file in cache:
        if log_id not in file:
            cache.remove(file)
    cache.sort()
    # now our cache is sorted by filename
    next_del_batch = cache[0:del_qty]
    cache = cache[del_qty:]
    if cache_file_path:
        if debug:
            print(f"writing cache file: {cache_file_path}", file=sys.stderr, flush=True)
        with open(cache_file_path, "w") as f:
            f.write("\n".join(cache))


def truncate_directory():
    global dry_run, debug, next_del_batch
    # cache has enough to meet delete spec
    for _file in next_del_batch:
        if debug:
            print(f"deleting: {_file}", file=sys.stderr, flush=True)
        if not dry_run:
            os.unlink(_file)


def main(argv):
    global directory, min_gig_freespace, current_free_space, sleep_time, cache_file_path, del_qty, debug, dry_run, log_id
    result = 1

    try:
        i = 1
        while i < len(argv):
            if i == 0:
                i += 1
            elif argv[i] == "--directory":
                i += 1
                directory = argv[i]
                i += 1
            elif argv[i] == "--del_qty":
                i += 1
                del_qty = int(argv[i])
                i += 1
            elif argv[i] == "--min_gig_freespace":
                i += 1
                min_gig_freespace = int(argv[i])
                i += 1
            elif argv[i] == "--log_id":
                i += 1
                log_id = argv[i]
                i += 1
            elif argv[i] == "--debug":
                i += 1
                debug = True
            elif argv[i] == "--dry_run":
                i += 1
                dry_run = True
            elif argv[i] == "--sleep_time":
                i += 1
                sleep_time = int(argv[i])
                i += 1
            elif argv[i] == "--cache_file_path":
                i += 1
                cache_file_path = argv[i]
                i += 1
            else:
                i += 1

        assert directory, "must enter directory"
        assert log_id, "must enter log_id"

        while True:
            check_freespace()
            while current_free_space < min_gig_freespace:
                check_filelist()
                truncate_directory()
                check_freespace()
            if debug:
                print(f"sleeping for {sleep_time} seconds", file=sys.stderr, flush=True)
            time.sleep(sleep_time)

        result = 0
    except (KeyboardInterrupt, SystemExit) as e:
        print(
            f"the process_manager_test was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"the process_manager_test was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )

    return result


if __name__ == "__main__":
    sys.exit(main(sys.argv))
