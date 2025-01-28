#!/usr/bin/python3
"""This module removes old version both locally and remotely."""

from fabric.api import env, local, run
import os

# Define the servers to connect to
env.hosts = ['100.26.214.60', '3.86.13.56']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep.
                      If 0 or 1, keeps only the most recent archive.
    """
    try:
        # Ensure number is an integer and defaults to at least 1
        number = int(number)
        if number <= 0:
            number = 1

        # Local clean-up: Keep the most recent `number` archives
        archives = sorted(os.listdir("versions"))
        archives_to_delete = archives[:-number]  # All except the last `number`
        for archive in archives_to_delete:
            local(f"rm -f versions/{archive}")

        # Remote clean-up: Perform the same on the servers
        run("mkdir -p /data/web_static/releases")  # Ensure the folder exists
        rel = run("ls -1t /data/web_static/releases | grep web_static").split()
        releases_to_delete = rel[number:]  # All except the first `number`
        for release in releases_to_delete:
            run(f"rm -rf /data/web_static/releases/{release}")
