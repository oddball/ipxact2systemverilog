import os

from lxml import etree

# CLI names are 1.5 and 2022. Schema directories follow the bundled XML packages.
IPXACT_VERSIONS = {
    "1.5": {
        "namespace": "http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5",
        "schema_dir": "ipxact-1.5",
    },
    "2022": {
        "namespace": "http://www.accellera.org/XMLSchema/IPXACT/1685-2022",
        "schema_dir": "ieee-1685-2022",
    },
}


def _namespace_uri(xml_tree):
    root = xml_tree.getroot()
    if root.tag.startswith("{") and "}" in root.tag:
        return root.tag.split("}", 1)[0][1:]
    raise ValueError("XML root element has no namespace; expected an IP-XACT component")


def detect_ipxact_version(xml_tree):
    namespace_uri = _namespace_uri(xml_tree)
    for version, info in IPXACT_VERSIONS.items():
        if namespace_uri == info["namespace"]:
            return version
    supported = ", ".join(IPXACT_VERSIONS)
    raise ValueError(f"Found unsupported IP-XACT namespace '{namespace_uri}'. Supported versions: {supported}")


def resolve_ipxact_version(xml_tree, xml_version=None):
    detected = detect_ipxact_version(xml_tree)
    if xml_version is None:
        return detected
    if xml_version not in IPXACT_VERSIONS:
        supported = ", ".join(IPXACT_VERSIONS)
        raise ValueError(f"Unsupported IP-XACT version '{xml_version}'. Supported versions: {supported}")
    if xml_version != detected:
        raise ValueError(f"IP-XACT file is version {detected}, but --xmlVersion {xml_version} was given")
    return detected


def ipxact_namespace(xml_version):
    return IPXACT_VERSIONS[xml_version]["namespace"]


def get_corresponding_schema(xml_tree, xml_version=None):
    version = resolve_ipxact_version(xml_tree, xml_version)
    schema_dir = IPXACT_VERSIONS[version]["schema_dir"]
    schema_file = os.path.join(os.path.dirname(__file__), "xml", schema_dir, "component.xsd")
    schema = etree.XMLSchema(file=schema_file)
    return schema


def validate(xmlfilename, xml_version=None):
    try:
        with open(xmlfilename, "r") as f:
            doc = etree.parse(f)

        schema = get_corresponding_schema(doc, xml_version)
        result = schema.validate(doc)

        if not result:
            print(schema.error_log)
        return result
    except FileNotFoundError:
        print(f"Error: XML file not found at '{xmlfilename}'")
        return False
    except ValueError as exc:
        print(exc)
        return False
