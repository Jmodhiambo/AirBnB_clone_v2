#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv

# Determine the type of storage to use
storage_type = getenv('HBNB_TYPE_STORAGE')  # Expected to be 'db' or 'file'

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
