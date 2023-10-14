"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __call__(self, approach):
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"


class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approaches):
        dates_only = approaches.time.date()
        return dates_only


class DistanceFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance


class VelocityFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity


class DiameterFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):

    filters = []
    # filter for date
    if date:
        date_filter = DateFilter(operator.eq, date)
        filters.append(date_filter)

    # filter for start date
    if start_date:
        start_date_filter = DateFilter(operator.ge, start_date)
        filters.append(start_date_filter)

    # filter for end date
    if end_date:
        end_date_filter = DateFilter(operator.le, end_date)
        filters.append(end_date_filter)

    # filter for min distance
    if distance_min:
        distance_min_filter = DistanceFilter(operator.ge, distance_min)
        filters.append(distance_min_filter)

    # filter for max distance
    if distance_max:
        distance_max_filter = DistanceFilter(operator.le, distance_max)
        filters.append(distance_max_filter)

    # filter for min velocity
    if velocity_min:
        velocity_min_filter = VelocityFilter(operator.ge, velocity_min)
        filters.append(velocity_min_filter)

    # filter for max velocity
    if velocity_max:
        velocity_max_filter = VelocityFilter(operator.le, velocity_max)
        filters.append(velocity_max_filter)

    # filter for min diameter
    if diameter_min:
        diameter_min_filter = DiameterFilter(operator.ge, diameter_min)
        filters.append(diameter_min_filter)

    # filter for max diameter
    if diameter_max:
        diameter_max_filter = DiameterFilter(operator.le, diameter_max)
        filters.append(diameter_max_filter)

    # filter for hazardous NEOs
    if hazardous == 'N':
        hazardous = False
    elif hazardous == 'Y':
        hazardous = True

    if hazardous is not None:
        hazardous_filter = HazardousFilter(operator.eq, hazardous)
        filters.append(hazardous_filter)

    return filters


def limit(iterator, args=None):
    start = 0
    for each_approach in iterator:
        if args is None or args == 0 or start < args:
            yield each_approach
            start += 1
        else:
            break
