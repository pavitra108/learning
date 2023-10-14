import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    collection_neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            designation = row['pdes']
            name = row['name']
            if name == '':
                name = None
            diameter = row['diameter']
            if row['pha'] == 'Y':
                hazardous = True
            else:
                hazardous = False
            neo_instance = NearEarthObject(designation, name, diameter, hazardous, approaches=[])
            collection_neos.append(neo_instance)
    return collection_neos


load_neos('data/neos.csv')


def load_approaches(cad_json_path):
    collection_cad = []
    with open(cad_json_path, 'r') as cadinfile:
        contents = json.load(cadinfile)
        fields = contents['fields']
        data = contents['data']
        output_list = list()
        for index, mainlist in enumerate(data):
            row_dict = dict()
            for index, item in enumerate(mainlist):
                row_dict[fields[index]] = item
            output_list.append(row_dict)

        for each_row in output_list:
            cad_designation = each_row['des']
            time = each_row['cd']
            distance = float(each_row['dist'])
            velocity = float(each_row['v_rel'])
            cad_instance = CloseApproach(cad_designation, time, distance, velocity, neo=[])
            collection_cad.append(cad_instance)
    return collection_cad


if __name__ == '__main__':
    load_approaches('data/cad.json')
