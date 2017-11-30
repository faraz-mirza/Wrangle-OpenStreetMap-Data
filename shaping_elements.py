# Fixing the Street names and Postal Codes while shaping all elements to generate csv files

import unicodecsv as csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus
import schema


OSM_PATH = "sample_san-francisco-bay_california.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
lower = re.compile(r'^([a-z]|_)*$')
one_colon = re.compile(r'^([a-z]|_|[A-Z]|[0-9])*:([a-z]|_|[A-Z]|[0-9])*$')
two_colon = re.compile(r'^([a-z]|_|[A-Z]|[0-9])*:([a-z]|_|[A-Z]|[0-9])*:([a-z]|_|[A-Z]|[0-9])*$')
one_hyphen = re.compile(r'^([a-z]|_|[A-Z]|[0-9])*-([a-z]|_|[A-Z]|[0-9])*$')

SCHEMA = schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Circle", "Terrace", "Way", "Gardens"]

mapping = {"St": "Street",
           "St.": "Street",
           "Ave": "Avenue",
           "Rd.": "Road",
           "Rd": "Road",
           "Dr": "Drive",
           "Blvd": "Boulevard",
           "Ct": "Court"
           }

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


def audit_street_type_update(street_name):
    lastWord = street_type_re.search(street_name)

    if lastWord:
        streetType = lastWord.group()

        if streetType not in expected:
            if streetType in mapping:
                street_name = re.sub(street_type_re, mapping[streetType], street_name)

    return street_name


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    tag_dict = {}

    if element.tag == 'node':
        for key, value in element.items():
            if key in node_attr_fields:
                node_attribs[key] = value

        for tag in element.iter("tag"):

            if PROBLEMCHARS.match(tag.attrib['k']) == None:
                tag_dict = {}

                tag_dict['id'] = node_attribs['id']

                if two_colon.match(tag.attrib['k']):
                    n = []
                    ty, pe, ky = tag.attrib['k'].split(":")
                    n.append(ty)
                    n.append(pe)
                    typ = ":".join(n)

                    tag_dict['type'] = typ
                    tag_dict['key'] = ky

                    tag_dict['value'] = tag.attrib['v']

                elif one_colon.match(tag.attrib['k']) == None:
                    tag_dict['type'] = default_tag_type
                    tag_dict['key'] = tag.attrib['k']

                    tag_dict['value'] = tag.attrib['v']


                else:
                    typ, ky = tag.attrib['k'].split(":")
                    tag_dict['type'] = typ
                    tag_dict['key'] = ky

                    if ky == "postcode":
                        if one_hyphen.match(tag.attrib['v']):
                            post, meh = tag.attrib['v'].split("-")
                            tag_dict['value'] = post

                        else:
                            tag_dict['value'] = tag.attrib['v']

                    elif tag.attrib['k'] == "addr:street":
                        newKy = audit_street_type_update(tag.attrib['v'])

                        tag_dict['value'] = newKy

                    else:
                        tag_dict['value'] = tag.attrib['v']

                tags.append(tag_dict)

        return {'node': node_attribs, 'node_tags': tags}


    elif element.tag == 'way':
        pos = -1

        for key, value in element.items():
            if key in way_attr_fields:
                way_attribs[key] = value

        for nd in element.iter("nd"):
            tag_dict = {}

            tag_dict['id'] = way_attribs['id']
            tag_dict['node_id'] = nd.attrib['ref']
            pos += 1
            tag_dict['position'] = pos

            way_nodes.append(tag_dict)

        for tag in element.iter("tag"):

            if PROBLEMCHARS.match(tag.attrib['k']) == None:
                tag_dict = {}

                tag_dict['id'] = way_attribs['id']

                if two_colon.match(tag.attrib['k']):
                    n = []
                    ty, pe, ky = tag.attrib['k'].split(":")
                    n.append(ty)
                    n.append(pe)
                    typ = ":".join(n)

                    tag_dict['type'] = typ
                    tag_dict['key'] = ky

                    tag_dict['value'] = tag.attrib['v']


                elif one_colon.match(tag.attrib['k']) == None:
                    tag_dict['type'] = default_tag_type
                    tag_dict['key'] = tag.attrib['k']

                    tag_dict['value'] = tag.attrib['v']



                else:
                    typ, ky = tag.attrib['k'].split(":", 1)
                    tag_dict['type'] = typ
                    tag_dict['key'] = ky

                    if ky == "postcode":
                        if one_hyphen.match(tag.attrib['v']):
                            post, meh = tag.attrib['v'].split("-")
                            tag_dict['value'] = post

                        else:
                            tag_dict['value'] = tag.attrib['v']

                    elif tag.attrib['k'] == "addr:street":
                        newKy = audit_street_type_update(tag.attrib['v'])

                        tag_dict['value'] = newKy

                    else:
                        tag_dict['value'] = tag.attrib['v']

                tags.append(tag_dict)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'wb') as nodes_file, codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, codecs.open(
            WAYS_PATH, 'wb') as ways_file, codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, codecs.open(
            WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


process_map(OSM_PATH, validate=False)