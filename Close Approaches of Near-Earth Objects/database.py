"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""


class NEODatabase:
    def __init__(self, neos, approaches):
        self._neos = neos
        self._approaches = approaches
        linked_neo_cad = {}
        # iterate each NEO
        for each_neo in self._neos:
            linked_neo_cad[each_neo.designation] = each_neo
        for each_cad in self._approaches:
            if each_cad._designation in linked_neo_cad:
                neo_obj = linked_neo_cad[each_cad._designation]
                each_cad.neo = neo_obj
                neo_obj.approaches.append(each_cad)

    def get_neo_by_designation(self, designation):
        for neo_obj in self._neos:
            if neo_obj.designation == designation:
                return neo_obj
        return None

    def get_neo_by_name(self, name):
        for neo_obj in self._neos:
            if neo_obj.name == name:
                return neo_obj
        return None

    def query(self, filters_objects):
        try:
            for approach in self._approaches:
                matched = True
                for filter_obj in filters_objects:
                    if not filter_obj(approach):
                        matched = False
                        break
                if matched:
                    yield approach
        except Exception as e:
            print(e)
