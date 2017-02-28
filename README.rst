ipxact2systemverilog ipxact2rst ipxact2vhdl
-------------------------------------------

This software takes an IP-XACT description of register banks, and generates synthesizable VHDL and SystemVerilog packages and ReStructuredText documents. It ONLY considers register bank descriptions. The software does not generate OVM or UVM testbench packages. In the example/tb directory there is an example of how to use the generated packages. 

Usage
-----

::
   
   pip3 install ipxact2systemverilog


::
   
   ipxact2systemverilog --srcFile FILE --destDir DIR
   ipxact2rst --srcFile FILE --destDir DIR
   ipxact2vhdl --srcFile FILE --destDir DIR


Testing the example file
------------------------
::
   
   make

If Modelsim is installed:
::
   
   make compile
   make sim


Note
----

From the reStructuredText file, together with http://docutils.sourceforge.net and http://rst2pdf.ralsina.com.ar it is possible to generate pdf and html files of the IP-XACT register bank descriptions.


Validation
----------
To validate your xml
::
   
   xmllint --noout --schema ipxact2systemverilog/xml/component.xsd  example/input/test.xml



Dependencies
------------

::
   
    pip3 install docutils
    pip3 install rst2pdf
    pip3 install lxml


TODO
----
* A better testbench for the generated packages should be implemented.
* More complicated IPXACT files should be added and tried out.
* Add support for the SystemVerilog generator to have a register field of an enumerated type.
* Use http://pyxb.sourceforge.net to enable dumping out the modified XML
* Support DIM
