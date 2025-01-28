#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to web servers.
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['100.26.214.60', '3.86.13.56']


def do_pack():
    """Packs the `web_static` folder into a .tgz archive."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = archive_path.split("/")[-1]
        archive_name = archive_file.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(archive_name)

        # Upload archive to /tmp/ directory
        put(archive_path, "/tmp/{}".format(archive_file))

        # Create release directory
        run("mkdir -p {}".format(release_path))

        # Unpack the archive into the release directory
        run("tar -xzf /tmp/{} -C {}".format(archive_file, release_path))

        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}".format(archive_file))

        # Move contents out of web_static subfolder
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove empty web_static directory
        run("rm -rf {}/web_static".format(release_path))

        # Remove the current symbolic link and recreate it
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Creates and deploys an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
