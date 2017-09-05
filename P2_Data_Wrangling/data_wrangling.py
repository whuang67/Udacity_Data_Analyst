# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 16:15:45 2017

@author: whuang67
"""

import os
import xml.etree.ElementTree as ET
import pprint
import re

### Load the data and check the size
os.chdir("C:/users/whuang67/downloads/detroit_michigan.osm")
OSM_FILE = "honolulu_hawaii.osm"
print "The size of our OSM file is {:.1f} megabytes.".format(
        os.path.getsize(OSM_FILE)/(1024.0**2))

### Check the postal codes
honolulu_zips = ["96801", "96802", "96803", "96804", "96805", "96806",
                 "96807", "96808", "96809", "96810", "96811", "96812",
                 "96813", "96814", "96815", "96816", "96817", "96818",
                 "96819", "96820", "96821", "96822", "96823", "96824",
                 "96825", "96826", "96828", "96830", "96836", "96837",
                 "96838", "96839", "96840", "96841", "96843", "96844",
                 "96846", "96847", "96848", "96849", "96850"] # Zipcodes from USPS

def count_zipcode(filename, verbose = True):
    output = {}
    keys = {"correct": 0, "wrong": 0}
    for _, elem in ET.iterparse(filename):
        if elem.attrib.get("k") == "addr:postcode":
            zipcode = elem.attrib.get("v")
            output[zipcode] = output.get(zipcode, 0) + 1
            if zipcode in honolulu_zips:
                keys["correct"] = keys.get("correct", 0) + 1
            else:
                keys["wrong"] = keys.get("wrong", 0) + 1
    if verbose == True:
        return output, keys
    else:
        return keys

output, keys = count_zipcode(OSM_FILE)
pprint.pprint(output)
pprint.pprint(keys)


### Clean the postal codes
def clean_zipcode(filename, cleaned_file):
    tree = ET.parse(filename)
    root = tree.getroot()
    delete = 0
    for child in ["node", "way", "relation"]:
        for elem in root.findall(child):
            for tag in elem.iter():
                if tag.get("k") == "addr:postcode":
                    zipcode = tag.get("v")
                    if zipcode not in honolulu_zips:
                        if len(zipcode) == 5 or zipcode == "9":
                            root.remove(elem)
                            delete += 1
                        elif len(zipcode) == 10:
                            if zipcode[0:5] in honolulu_zips:
                                tag.set("v", zipcode[0:5])
                            else:
                                root.remove(elem)
                                delete += 1
                        else:
                            tag.set("v", "96819") ### ONlY one -- HI 96819
    print "{} records were removed.".format(delete)
    return tree.write(cleaned_file)

cleaned_postal_file = 'cleaned_postal_file.xml'
clean_zipcode(OSM_FILE, cleaned_postal_file)
### Double check if postal codes are clean
print "\nDouble check the dataset after being cleaned:"
pprint.pprint(count_zipcode(cleaned_postal_file, verbose = False))


### Clean the formats of phone numbers
def clean_phone_number(filename, cleaned_file):
    tree = ET.parse(filename)
    root = tree.getroot()
    for tag in root.findall('*/tag'):
        if tag.attrib["k"] == "phone":
            phone = tag.attrib["v"]
            # print phone
            new_phone = re.sub(r"[\D|\s]+", "", phone)
            if len(new_phone) == 11:
                tag.set("v", new_phone[-10: -7]+"-"+new_phone[-7: -4]+"-"+new_phone[-4:])
                # print tag.attrib["v"]
            elif len(new_phone) == 20:
                tag.set("v", "808-284-1270, 808-271-4836")
                # print tag.attrib["v"]
            elif len(new_phone) == 10:
                tag.set("v", new_phone[0:3]+"-"+new_phone[3:6]+"-"+new_phone[6:])
                # print tag.attrib["v"]
            else:
                tag.set("v", "808-"+new_phone[0:3]+"-"+new_phone[3:])
    return tree.write(cleaned_file)

cleaned_phone_file = "cleaned_phone_file.xml"
clean_phone_number(cleaned_postal_file, cleaned_phone_file)


### Double check if phone number formats are good
cleaned_phone_re = re.compile(r"\d{3}-\d{3}-\d{4}$")
def check_phone_number(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    nothing = True
    for tag in root.findall('*/tag'):
        if tag.attrib["k"] == "phone":
            phone = tag.attrib["v"]
            if not cleaned_phone_re.match(phone):
                if phone != "808-284-1270, 808-271-4836":
                    nothing = False
                    print phone
    if nothing == True:
        print "There is nothing wrong!"

# print check_phone_number(cleaned_postal_file)
print check_phone_number(cleaned_phone_file)


### Clean the street abbreviations
##### Helpful functions
from collections import defaultdict
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = {"s": "South",
           "n": "North",
           "e": "East",
           "w": "West",
           "pl": "Place",
           "st": "Street",
           "ave": "Avenue",
           "rd": "Road",
           "blvd":"Boulevard",
           "sr": "Drive",
           "ct": "Court",
           "ne": "Northeast",
           "se": "Southeast",
           "nw": "Northwest",
           "sw": "Southwest",
           "dr": "Drive",
           "sq": "Square",
           "ln": "Lane",
           "trl": "Trail",
           "pkwy": "Parkway",
           "ste": "Suite",
           "lp": "Loop",
           "hwy": "Highway"}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def update_name(name, mapping):
    name_list = name.split()
    for i in range(len(name_list)):
        word = name_list[i].lower()
        if word in mapping.keys():
            name_list[i] = mapping[word]
    better_name = " ".join(name_list)
    return better_name

st_types = audit(cleaned_phone_file)

count = 0
for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        if name != better_name:
            print name, "=>", better_name
            count += 1

### Clean the street abbreviations
def clean_address(filename, cleaned_file):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    for tag in root.findall("*/tag"):
        if is_street_name(tag):
            name = tag.get("v")
            better_name = update_name(name, mapping)
            tag.set("v", better_name)
    return tree.write(cleaned_file)

cleaned_street_file = 'cleaned_street_name.xml'
clean_address(cleaned_phone_file, cleaned_street_file)

### Print out the old and new street names
st_types = audit(cleaned_street_file)

count = 0
for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        if name != better_name and count <= 10:
            print name, "=>", better_name
            count += 1


### Convert the OSM into CSV
import csv
import codecs
import cerberus
import schema

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset',
               'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def load_new_tag(element, secondary, default_tag_type):
    new = {}
    new['id'] = element.attrib["id"]
    if ":" not in secondary.attrib["k"]:
        new["key"] = secondary.attrib["k"]
        new["type"] = default_tag_type
    else:
        post_colon = secondary.attrib['k'].index(":") + 1
        new['key'] = secondary.attrib['k'][post_colon:]
        new['type'] = secondary.attrib['k'][:post_colon - 1]
    new['value'] = secondary.attrib["v"]
    return new
        
def shape_element(element,
                  node_attr_fields = NODE_FIELDS,
                  way_attr_fields = WAY_FIELDS,
                  problem_chars = PROBLEMCHARS,
                  default_tag_type = 'regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    counter = 0
    # YOUR CODE HERE
    if element.tag == 'node':
        for attrib, value in element.attrib.iteritems():
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = value
        
        for secondary in element.iter():
            if secondary.tag == "tag":
                if problem_chars.match(secondary.attrib["k"]) is not None:
                    continue
                else:
                    new = load_new_tag(element, secondary, default_tag_type)
                    if new is not None:
                        tags.append(new)
        # print {'node': node_attribs, 'node_tags': tags}        
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        for attrib, value in element.attrib.iteritems():
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = value
        
        for secondary in element.iter():
            if secondary.tag == "nd":
                newnd = {}
                newnd['id'] = element.attrib['id']
                newnd['node_id'] = secondary.attrib['ref']
                newnd['position'] = counter
                counter += 1
                way_nodes.append(newnd)
            elif secondary.tag == "tag":
                if problem_chars.match(secondary.attrib["k"]) is not None:
                    continue
                else:
                    new = load_new_tag(element, secondary, default_tag_type)
                    if new is not None:
                        tags.append(new)
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
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) \
            for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

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

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(cleaned_street_file, validate=False)

print "The size of our nodes.csv file is {:.1f} megabytes.".format(
        os.path.getsize(NODES_PATH)/(1024.0**2))
print "The size of our nodes_tags.csv file is {:.1f} megabytes.".format(
        os.path.getsize(NODE_TAGS_PATH)/(1024.0**2))
print "The size of our ways.csv file is {:.1f} megabytes.".format(
        os.path.getsize(WAYS_PATH)/(1024.0**2))
print "The size of our ways_nodes.csv file is {:.1f} megabytes.".format(
        os.path.getsize(WAY_NODES_PATH)/(1024.0**2))
print "The size of our ways_tags.csv file is {:.1f} megabytes.".format(
        os.path.getsize(WAY_TAGS_PATH)/(1024.0**2))