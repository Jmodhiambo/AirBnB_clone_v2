#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import os


# Table for Many-To-Many relationship between Place and Amenity
place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False
    )
)


class Place(BaseModel, Base):
    """ A place to stay by various attributes """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            back_populates="place",
            cascade="all, delete-orphan"
        )

        amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False
        )
    else:
        @property
        def reviews(self):
            """ Returns the list of Review instances with
            place_id equals current Place.id
            """
            from models import storage
            all_reviews = storage.all("Review")
            return [
                review for review in all_reviews.values()
                if review.place_id == self.id
            ]

        @property
        def amenities(self):
            """ Returns the list of Amenity instances linked to the Place """
            from models import storage
            from models.amenity import Amenity
            all_amenities = storage.all(Amenity)
            return [
                amenity for amenity in all_amenities.values()
                if amenity.id in self.amenity_ids
            ]

        @amenities.setter
        def amenities(self, obj):
            """ Appends Amenity.id to the amenity_ids list
            if obj is an Amenity """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
