#!/usr/bin/python3
"""DBStorage module for HBNB project"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Database storage engine for HBNB"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database storage engine"""
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        PWD = HBNB_MYSQL_PWD  # Shortened to avoid PEP error
        DB = HBNB_MYSQL_DB

        # Create engine
        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{PWD}@{HBNB_MYSQL_HOST}/{DB}",
            pool_pre_ping=True,
            echo=True
        )

        # Drop tables if the environment is "test"
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects or objects of a specific class"""
        obj_dict = {}
        objs = []
        if cls:
            objs = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                objs.extend(self.__session.query(cls).all())

        for obj in objs:
            key = f"{obj.__class__.__name__}.{obj.id}"
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add object to the current session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def get(self, cls, id):
        """Retrieve an object by class name and id."""
        if not cls or not id:
            return None

        if isinstance(cls, str):
            from models import classes
            cls = classes.get(cls, None)  # Map class name to class object
            if not cls:
                return None

        return self.__session.query(cls).get(id)

    def close(self):
        """Remove or close the current SQLAlchemy session."""
        self.__session.remove()  # Alternative: self.__session.close()
