#!/usr/bin/env python3
import os
from lxml import etree

def extractIpxactVersion(XMLtree):
    root = XMLtree.getroot()
    if root.tag.startswith('{') and '}' in root.tag:
        namespace_uri = root.tag.split('}', 1)[0][1:]
        version = namespace_uri.split('/')[-1]
        if version == "1.5":
            return version
        else:
            raise Exception(f"Found unsupported IP-XACT version: '{version}', Only supported version: '1.5'")



def getCorrespondingSchema(XMLtree):
    ipxact_version = extractIpxactVersion(XMLtree)
    schema_file = os.path.join(os.path.dirname(__file__), 'xml', f'ipxact-{ipxact_version}', 'component.xsd')
    schema = etree.XMLSchema(file=schema_file)
    return schema


def validate(xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
            doc = etree.parse(f)

        schema = getCorrespondingSchema(doc)
        result = schema.validate(doc)

        if not result:
            print(schema.error_log)
        return result
    except FileNotFoundError:
        print(f"Error: XML file not found at '{xmlfilename}'")
        return False