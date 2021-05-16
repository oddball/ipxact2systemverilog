ipxact2systemverilog ipxact2rst ipxact2md ipxact2vhdl
-----------------------------------------------------

.. image:: https://circleci.com/gh/oddball/ipxact2systemverilog.svg?style=shield&circle-token=071d263d097ebb33943a749ecb66549c9f0512ed
   :target: https://circleci.com/gh/oddball/ipxact2systemverilog

.. image:: https://pypip.in/v/ipxact2systemverilog/badge.svg
        :target: https://pypi.python.org/pypi/ipxact2systemverilog/

This software takes an IP-XACT description of register banks, and generates synthesizable VHDL and SystemVerilog packages and ReStructuredText documents. It ONLY considers register bank descriptions. The software does not generate OVM or UVM testbench packages. In the example/tb directory there is an example of how to use the generated packages. 

Usage
-----

::
   
   pip install ipxact2systemverilog


::
   
   ipxact2systemverilog --srcFile FILE --destDir DIR
   ipxact2rst --srcFile FILE --destDir DIR
   ipxact2md --srcFile FILE --destDir DIR
   ipxact2vhdl --srcFile FILE --destDir DIR


Development
-----------
See https://github.com/oddball/ipxact2systemverilog

Testing the example file
========================
::
   
   make

If Modelsim is installed:
::
   
   make compile
   make sim


Note
====
You can use http://pandoc.org/demos.html to convert to almost any fileformat.


Validation
==========
To validate your xml
::
   
   xmllint --noout --schema ipxact2systemverilog/xml/component.xsd  example/input/test.xml



Dependencies
============

::
   
    pip install docutils lxml tabulate mdutils


Dependencies used by makefile
=============================
These are not needed for ipxact2systemverilog, but used for generating some of the files in example/output

::
   
   brew install pandoc


Working in development mode for pypi
====================================

::
   
   rm -rf dist
   pip3 install -e .
   python3 setup.py sdist
   twine upload dist/*

   

TODO
====
* A better testbench for the generated packages should be implemented.
* More complicated IPXACT files should be added and tried out.
* Add support for the SystemVerilog generator to have a register field of an enumerated type.
* Support DIM

