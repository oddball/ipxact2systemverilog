========
example2
========

Second demo example used for the testing of the ipxact2systemverilog
tool.

:Base Address: 0x0

Registers
---------

+-----------+-----------------+--------------------------------+
| Address   | Register Name   | Description                    |
+===========+=================+================================+
| 0x00      | reg0_           | read something useful for reg0 |
+-----------+-----------------+--------------------------------+
| 0x01      | reg1_           |                                |
+-----------+-----------------+--------------------------------+

reg0
----

:Name: reg0
:Address: 0x0
:Access: read-only
:Description: read something useful for reg0

+--------+--------------+----------------------------------+
| Bits   | Field name   | Description                      |
+========+==============+==================================+
| [7:2]  | field1       | read something useful for field1 |
+--------+--------------+----------------------------------+
| [1:0]  | field0       | read something useful for field0 |
+--------+--------------+----------------------------------+

reg1
----

:Name: reg1
:Address: 0x1
:Access: read-only
:Description:

+--------+--------------+----------------------------------+
| Bits   | Field name   | Description                      |
+========+==============+==================================+
| [7:0]  | field0       | read something useful for field0 |
+--------+--------------+----------------------------------+

