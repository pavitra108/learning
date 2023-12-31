"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as outfile:
        fields = ['datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km',
                  'potentially_hazardous']
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        for each_obj in results:
            time = each_obj.time
            distance = each_obj.distance
            velocity = each_obj.velocity
            designation = each_obj.neo.designation
            name = each_obj.neo.name
            diameter = each_obj.neo.diameter
            hazardous = each_obj.neo.hazardous
            my_dict = {'datetime_utc': time, 'distance_au': distance,
                       'velocity_km_s': velocity, 'designation': designation,
                       'name': name, 'diameter_km': diameter, 'potentially_hazardous': hazardous}
            writer.writerow(my_dict)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data_list = []
    for each_obj in results:
        time = each_obj.time
        distance = each_obj.distance
        velocity = each_obj.velocity
        designation = each_obj.neo.designation
        name = each_obj.neo.name
        diameter = each_obj.neo.diameter
        hazardous = each_obj.neo.hazardous
        formatted_time = time.strftime("%Y-%m-%d %H:%M")
        my_json_dict = {'datetime_utc': formatted_time, 'distance_au': distance,
                        'velocity_km_s': velocity,
                        'neo': {'designation': designation, 'name': name,
                                'diameter_km': diameter, 'potentially_hazardous': hazardous}}
        data_list.append(my_json_dict)
    with open(filename, 'w') as outfile:
        json.dump(data_list, outfile, indent=2)
