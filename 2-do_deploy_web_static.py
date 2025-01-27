#!/usr/bin/python3
"""
This module contains the function `do_deploy` that distributes an archive
to two web servers (xx-web-01 and xx-web-02).
"""

from fabric.api import put, run, env
import os

# Define web server IPs for both web servers
env.hosts = ['100.26.214.60', '3.86.13.56']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Returns False if the archive does not exist or any errors occur.
    """

    # Check if the file exists
    if not os.path.exists(archive_path):
        print(f"Error: {archive_path} does not exist.")
        return False

    # Define the name of the archive without the path
    archive_name = os.path.basename(archive_path)

    # Define the release directory (without the .tgz extension)
    release_dir = f"/data/web_static/releases/{archive_name.split('.')[0]}"

    try:
        # Upload the archive to the /tmp directory on the remote server
        put(archive_path, f"/tmp/{archive_name}")

        # Create the directory for the release
        run(f"sudo mkdir -p {release_dir}")

        # Uncompress the archive to the release directory
        run(f"sudo tar -xzf /tmp/{archive_name} -C {release_dir}")

        # Remove the archive from the remote server
        run(f"sudo rm /tmp/{archive_name}")

        # Move files from the web_static folder to the release directory
        run(f"sudo mv {release_dir}/web_static/* {release_dir}/")

        # Delete the now-empty web_static folder in the release directory
        run(f"sudo rm -rf {release_dir}/web_static")

        # Delete the symbolic link for the current version
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new release
        run(f"sudo ln -s {release_dir} /data/web_static/current")

        # Reload Nginx to apply the changes
        run("sudo systemctl reload nginx")

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
