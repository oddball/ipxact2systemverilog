#!/usr/bin/env python3

import os
from lxml import etree

schema_file = os.path.join(os.path.dirname(__file__), 'xml', 'component.xsd')
schema = etree.XMLSchema(file=schema_file)

def validate(xmlfilename):
    f = open(xmlfilename, 'r')
    doc = etree.parse(f)
    return schema.validate(doc)


