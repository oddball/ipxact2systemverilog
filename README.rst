ipxact2systemverilog ipxact2rst ipxact2vhdl
-------------------------------------------

This software takes an IP-XACT description of register banks, and generates synthesizable VHDL and SystemVerilog packages and ReStructuredText documents. It ONLY considers register bank descriptions. The software does not generate OVM or UVM testbench packages. In the tb directory there is an example of how to use the generated packages. 

Usage
-----

ipxact2systemverilog.py --srcFile FILE --destDir DIR

ipxact2rst.py --srcFile FILE --destDir DIR

ipxact2vhdl.py --srcFile FILE --destDir DIR


Testing the example file
------------------------

make

If Modelsim is installed:

make compile

make sim


Note
----

From the reStructuredText file, together with 

http://docutils.sourceforge.net 

and http://rst2pdf.ralsina.com.ar 

it is possible to generate pdf and html files of the IP-XACT register bank descriptions.


TODO
----
* A better testbench for the generated packages should be implemented.
* More complicated IPXACT files should be added and tried out.
* Add support for the SystemVerilog generator to have a register field of an enumerated type.
* Use http://pyxb.sourceforge.net to enable dumping out the modified XML
* Support DIM
