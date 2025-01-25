#!/usr/bin/python3
"""
This module contains a function `do_pack` that generates a .tgz archive
from the contents of the `web_static` folder. The generated archive is
stored in the `versions` folder with a timestamped filename.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """

    # Create the 'versions' directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the current timestamp for naming the archive
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Define the archive name and path
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = os.path.join("versions", archive_name)

    # Create the .tgz archive of the web_static folder
    try:
        local(f"tar -cvzf {archive_path} web_static")
        print(f"Packing web_static to {archive_path}")
        return archive_path
    except Exception as e:
        print(f"An error occurred while creating the archive: {e}")
        return None
