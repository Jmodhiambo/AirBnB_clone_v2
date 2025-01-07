#!/usr/bin/python3

from models.engine.file_storage import FileStorage
from models.state import State

storage = FileStorage()
print("Testing delete method...")

# Create and add State object
state = State(name="California")
storage.new(state)
storage.save()

# Verify the object exists
print("Before deletion:", storage.all())

# Test deletion
storage.delete(state)
print("After deletion:", storage.all())

# Test delete with None
storage.delete(None)
