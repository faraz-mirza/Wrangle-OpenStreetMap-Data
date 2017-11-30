# Categorization of Data
import re
import xml.etree.cElementTree as ET


SAMPLE_FILE = "sample_san-francisco-bay_california.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
two_colon = re.compile(r'^([a-z]|_|[A-Z]|[0-9])*:([a-z]|_|[A-Z]|[0-9])*:([a-z]|_|[A-Z]|[0-9])*$')


def key_type(element, keys):
    if element.tag == "tag":
        for ele in element.iter():
            eleTemp = ele.attrib['k']

            if lower.match(eleTemp) != None:
                keys['lower'] += 1
            elif lower_colon.match(eleTemp) != None:
                keys['lower_colon'] += 1
            elif two_colon.match(eleTemp) != None:
                keys['two_colon'] += 1
            elif problemchars.findall(eleTemp) != []:
                keys['problemchars'] += 1
            else:
                keys['other'] += 1

    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "two_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


keys = process_map(SAMPLE_FILE)

print (keys)
