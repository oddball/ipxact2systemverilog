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
| 0x1d      | samename_       | samename register              |
+-----------+-----------------+--------------------------------+

.. _reg_reg0:

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

.. _reg_reg1:

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

field0
~~~~~~

:Minimum: 0x00
:Maximum: 0x07

.. _reg_samename:

samename
--------

:Name: samename
:Address: 0x1d
:Reset Value: 0x00
:Access: read-only
:Description: samename register

+--------+--------------+---------+---------------+
| Bits   | Field name   | Reset   | Description   |
+========+==============+=========+===============+
| [7:2]  | unused0      | 0x00    | unused        |
+--------+--------------+---------+---------------+
| [1:0]  | samename     | 0x0     |               |
+--------+--------------+---------+---------------+

.. _enum_samename:

samename
~~~~~~~~

+--------+---------+---------------+
| Name   | Value   | Description   |
+========+=========+===============+
| a      | 0x0     | a             |
+--------+---------+---------------+
| b      | 0x1     | b             |
+--------+---------+---------------+
| c      | 0x2     | c             |
+--------+---------+---------------+
| d      | 0x3     | d             |
+--------+---------+---------------+

