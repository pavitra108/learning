from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    def __init__(self, designation, name, diameter, hazardous, approaches):
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
        return {
            "designation": self.designation,
            "name": self.name,
            "hazardous": self.hazardous,
            "diameter": self.diameter,
            "approaches": self.approaches
        }

    @property
    def fullname(self):
        full_name = f"{self.designation} {self.name}"
        return full_name

    def __str__(self):
        status = "is" if self.hazardous else "is not"
        neo_details = f"A NEO {self.fullname} has a diameter of {self.diameter} km and {status} potentially hazardous."
        return neo_details

    def __repr__(self):
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    def __init__(self, designation, time, distance, velocity, neo):
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.neo = neo

    def to_cad_dict(self):
        return {
            "designation": self._designation,
            "time": self.time,
            "distance": self.distance,
            "velocity": self.velocity,
            "neo": self.neo
        }

    @property
    def time_str(self):
        converted_time = datetime_to_str(self.time)
        return converted_time

    def __str__(self):
        approaches_details = f"On {self.time_str}, NEO {self._designation} approaches Earth at a distance of {self.distance} au and a velocity of {self.velocity} km/s."
        return approaches_details

    def __repr__(self):
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
