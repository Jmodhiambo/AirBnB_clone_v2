#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    # Many-To-Many relationship with Place
    place_amenities = relationship(
        "Place",
        secondary="place_amenity",
        viewonly=True
    )
