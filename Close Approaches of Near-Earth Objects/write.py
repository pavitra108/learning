import csv
import json


def write_to_csv(results, filename):
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
