#!/usr/bin/env python

from optparse import OptionParser
import glob
import os
import xml.etree.ElementTree as etree
import textwrap
from ipxact2hdlCommon import *

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--srcFile", dest="srcFile",
                      help="", metavar="FILE")
    parser.add_option("-d", "--destDir", dest="destDir",
                      help="write generated file to DIR", metavar="DIR")
    (options, args) = parser.parse_args()
    e = ipxactParser(options.srcFile)
    document = e.returnDocument()
    generator = ipxact2otherGenerator(options.destDir)
    generator.generate(vhdlAddressBlock,document)




