import argparse
import configparser
import sys

from .ipxact2hdlCommon import (
    DEFAULT_INI,
    CAddressBlock,
    Ipxact2OtherGenerator,
    IpxactParser,
    MdAddressBlock,
    PyAddressBlock,
    RstAddressBlock,
    SystemVerilogAddressBlock,
    VhdlAddressBlock,
)
from .validate import validate


def _prepare(description):
    parser = argparse.ArgumentParser(description=description)
    # Flag names stay camelCase so existing command lines keep working.
    parser.add_argument("-s", "--srcFile", dest="src_file", help="ipxact xml input file", required=True)
    parser.add_argument("-d", "--destDir", dest="dest_dir", help="write generated file to dir", required=True)
    parser.add_argument("-c", "--config", help="configuration ini file")
    parser.add_argument(
        "--xmlVersion",
        dest="xml_version",
        choices=["1.5", "2022"],
        default="1.5",
        help="IP-XACT version of the input file (default: 1.5)",
    )

    args, _ = parser.parse_known_args()

    if not validate(args.src_file, args.xml_version):
        print(f"{args.src_file} doesn't validate")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_INI)
    if args.config:
        config.read(args.config)
    return args, config


def _generate(description, generator_class):
    args, config = _prepare(description)
    document = IpxactParser(args.src_file, config, args.xml_version).return_document()
    Ipxact2OtherGenerator(args.dest_dir, config).generate(generator_class, document)


def main_c():
    _generate("ipxact2c", CAddressBlock)


def main_md():
    _generate("ipxact2md", MdAddressBlock)


def main_rst():
    _generate("ipxact2rst", RstAddressBlock)


def main_systemverilog():
    _generate("ipxact2systemverilog", SystemVerilogAddressBlock)


def main_vhdl():
    _generate("ipxact2vhdl", VhdlAddressBlock)


def main_py():
    _generate("ipxact2python", PyAddressBlock)
