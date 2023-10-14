"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name, diameter, hazardous, approaches):
        """Create a new `NearEarthObject`.

        :designation: designation
        :name: name of the neo
        :diameter: diameter of the neo
        :hazardous: bool to check if it is hazardous
        :approaches: approaches
        """
        self.designation = designation
        if name is None:
            self.name = None
        else:
            self.name = name
        self.name = name
        if diameter == '' or diameter is None:
            self.diameter = float('nan')
        else:
            self.diameter = float(diameter)
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = approaches

    def to_neo_dict(self):
        """Return the dict containing few params."""
        return {
            "designation": self.designation,
            "name": self.name,
            "hazardous": self.hazardous,
            "diameter": self.diameter,
            "approaches": self.approaches
        }

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        full_name = f"{self.designation} {self.name}"
        return full_name

    def __str__(self):
        """Return `str(self)`."""
        status = "is" if self.hazardous else "is not"
        neo_details = f"A NEO {self.fullname} has a diameter of {self.diameter} km and {status} potentially hazardous."
        return neo_details

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time, distance, velocity, neo):
        """Create a new `CloseApproach`.

        :param designation: designation.
        :param time: time
        :param distance: distance
        :param velocity: velocity
        :param neo: neo
        """
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.neo = neo

    def to_cad_dict(self):
        """Return a dict."""
        return {
            "designation": self._designation,
            "time": self.time,
            "distance": self.distance,
            "velocity": self.velocity,
            "neo": self.neo
        }

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        converted_time = datetime_to_str(self.time)
        return converted_time

    def __str__(self):
        """Return `str(self)`."""
        approaches_details = f"On {self.time_str}, NEO {self._designation} approaches Earth at a distance of {self.distance} au and a velocity of {self.velocity} km/s."
        return approaches_details

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
