# Auditing and updating the Street Names

import re
from collections import defaultdict
import xml.etree.cElementTree as ET


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
OSMFILE = "sample_san-francisco-bay_california.osm"

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Circle", "Terrace", "Way", "Gardens"]

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Rd.": "Road",
           "Rd": "Road",
           "Dr": "Drive",
           "Ct": "Court",
           "Blvd": "Boulevard"
           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(OSMFILE, "rb")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]

    name = ' '.join(name)

    return name


st_types = audit(OSMFILE)

for st_type, ways in st_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print(str(name) + " => " + str(better_name))
