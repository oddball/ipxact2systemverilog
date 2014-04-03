====================
Register description
====================

Registers
---------

+--------+---------------+----------------------------------------+
|Address |Register Name  |Description                             |
+========+===============+========================================+
|0x00    |reg0_          |write something usefull for reg0        |
+--------+---------------+----------------------------------------+
|0x01    |reg1_          |write something usefull for reg0        |
+--------+---------------+----------------------------------------+
|0x02    |reg2_          |write something usefull for reg0        |
+--------+---------------+----------------------------------------+
|0x03    |reg3_          |write something usefull for reg3        |
+--------+---------------+----------------------------------------+
|0x04    |reg4_          |reg4 is a very usefull register. It can |
|        |               |take down the moon when configured      |
|        |               |correctly.                              |
+--------+---------------+----------------------------------------+
|0x05    |reg5_          |reg5 is as usefull as reg4 but without a|
|        |               |reset value defined.                    |
+--------+---------------+----------------------------------------+
|0x06    |reg6_          |reg6 is a read only register.           |
+--------+---------------+----------------------------------------+

reg0
----

:Name:        reg0
:Address:     0x0
:Reset Value: 0x00000000
:Access:      read-write
:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:24]     |byte3          |          |write something     |
|            |               |          |usefull for field3  |
+------------+---------------+----------+--------------------+
|[23:16]     |byte2          |          |write something     |
|            |               |          |usefull for field3  |
+------------+---------------+----------+--------------------+
|[15:8]      |byte1          |          |write something     |
|            |               |          |usefull for field1  |
+------------+---------------+----------+--------------------+
|[7:0]       |byte0          |          |write something     |
|            |               |          |usefull for field0  |
+------------+---------------+----------+--------------------+

reg1
----

:Name:        reg1
:Address:     0x1
:Reset Value: 0x00000001
:Access:      read-write
:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:0]      |field0         |          |write something     |
|            |               |          |usefull for field0  |
+------------+---------------+----------+--------------------+

reg2
----

:Name:        reg2
:Address:     0x2
:Reset Value: 0x00000001
:Access:      read-write
:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[5:4]       |monkey2        |chimp=0,  |which monkey        |
|            |               |gorilla=1,|                    |
|            |               |phb=2     |                    |
+------------+---------------+----------+--------------------+
|[3:2]       |monkey         |chimp=0,  |which monkey        |
|            |               |gorilla=1,|                    |
|            |               |phb=2     |                    |
+------------+---------------+----------+--------------------+
|[1:1]       |power2         |          |write something     |
|            |               |          |usefull for field   |
|            |               |          |power2              |
+------------+---------------+----------+--------------------+
|[0:0]       |power          |          |write something     |
|            |               |          |usefull for field   |
|            |               |          |power               |
+------------+---------------+----------+--------------------+

reg3
----

:Name:        reg3
:Address:     0x3
:Reset Value: 0x00000001
:Access:      read-write
:Description: write something usefull for reg3

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:0]      |field0         |          |write something     |
|            |               |          |usefull for field0  |
+------------+---------------+----------+--------------------+

reg4
----

:Name:        reg4
:Address:     0x4
:Reset Value: 0x0000000c
:Access:      read-write
:Description: reg4 is a very usefull register. It can take down the moon when configured correctly.

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:0]      |reg4           |          |                    |
+------------+---------------+----------+--------------------+

reg5
----

:Name:        reg5
:Address:     0x5
:Access:      read-write
:Description: reg5 is as usefull as reg4 but without a reset value defined.

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:0]      |reg5           |          |                    |
+------------+---------------+----------+--------------------+

reg6
----

:Name:        reg6
:Address:     0x6
:Access:      read-only
:Description: reg6 is a read only register.

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         |
+============+===============+==========+====================+
|[31:0]      |reg6           |          |                    |
+------------+---------------+----------+--------------------+

