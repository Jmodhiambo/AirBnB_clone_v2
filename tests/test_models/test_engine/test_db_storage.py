import unittest
import os
from models import storage
from models.engine.db_storage import DBStorage
from models.state import State
from models.city import City
from sqlalchemy.exc import IntegrityError


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage tests")
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage class"""

    def setUp(self):
        """Set up test cases"""
        self.storage = storage
        self.state = State(name="TestState")
        self.city = City(name="TestCity", state_id=self.state.id)

    def tearDown(self):
        """Clean up test cases"""
        try:
            self.storage.delete(self.city)
            self.storage.delete(self.state)
            self.storage.save()
        except Exception:
            pass

    def test_all(self):
        """Test the all() method"""
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)

    def test_new_and_save(self):
        """Test the new() and save() methods"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.state, self.storage.all(State).values())

        self.storage.new(self.city)
        self.storage.save()
        self.assertIn(self.city, self.storage.all(City).values())

    def test_delete(self):
        """Test the delete() method"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.state, self.storage.all(State).values())

        self.storage.delete(self.state)
        self.storage.save()
        self.assertNotIn(self.state, self.storage.all(State).values())

    def test_reload(self):
        """Test the reload() method"""
        self.storage.new(self.state)
        self.storage.save()
        self.storage.reload()
        self.assertIn(
            self.state.id,
            [obj.id for obj in self.storage.all(State).values()]
        )

    def test_integrity_error(self):
        """Test handling of integrity errors"""
        state_duplicate = State(id=self.state.id, name="DuplicateState")
        self.storage.new(self.state)
        self.storage.save()
        with self.assertRaises(IntegrityError):
            self.storage.new(state_duplicate)
            self.storage.save()


if __name__ == "__main__":
    unittest.main()
