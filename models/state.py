#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class, contains name and cities """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            back_populates="state",
            cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """Getter for cities related to this state (FileStorage only)."""
            from models.city import City
            from models import storage
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list  # Returns a list of city instances
