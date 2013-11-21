====================
Register description
====================

Registers
---------

+------------+---------------+
|Address     |Register Name  +
+============+===============+
|0x0         |reg0_          +
+------------+---------------+
|0x1         |reg1_          +
+------------+---------------+
|0x2         |reg2_          +
+------------+---------------+
|0x3         |reg3_          +
+------------+---------------+
|0x4         |reg4_          +
+------------+---------------+

reg0
----

:Name:        reg0

:Address:     0x0

:Reset Value: 0x0

:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         +
+============+===============+==========+====================+
|[31:24]     |byte3          |          |write something     +
|            |               |          |usefull for field3  +
+------------+---------------+----------+--------------------+
|[23:16]     |byte2          |          |write something     +
|            |               |          |usefull for field3  +
+------------+---------------+----------+--------------------+
|[15:8]      |byte1          |          |write something     +
|            |               |          |usefull for field1  +
+------------+---------------+----------+--------------------+
|[7:0]       |byte0          |          |write something     +
|            |               |          |usefull for field0  +
+------------+---------------+----------+--------------------+

reg1
----

:Name:        reg1

:Address:     0x1

:Reset Value: 0x1

:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         +
+============+===============+==========+====================+
|[31:0]      |field0         |          |write something     +
|            |               |          |usefull for field0  +
+------------+---------------+----------+--------------------+

reg2
----

:Name:        reg2

:Address:     0x2

:Reset Value: 0x1

:Description: write something usefull for reg0

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         +
+============+===============+==========+====================+
|[5:4]       |monkey2        |chimp=0,  |which monkey        +
|            |               |gorilla=1,|                    +
|            |               |phb=2     |                    +
+------------+---------------+----------+--------------------+
|[3:2]       |monkey         |chimp=0,  |which monkey        +
|            |               |gorilla=1,|                    +
|            |               |phb=2     |                    +
+------------+---------------+----------+--------------------+
|[1:1]       |power2         |          |write something     +
|            |               |          |usefull for field   +
|            |               |          |power2              +
+------------+---------------+----------+--------------------+
|[0:0]       |power          |          |write something     +
|            |               |          |usefull for field   +
|            |               |          |power               +
+------------+---------------+----------+--------------------+

reg3
----

:Name:        reg3

:Address:     0x3

:Reset Value: 0x1

:Description: write something usefull for reg3

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         +
+============+===============+==========+====================+
|[31:0]      |field0         |          |write something     +
|            |               |          |usefull for field0  +
+------------+---------------+----------+--------------------+

reg4
----

:Name:        reg4

:Address:     0x4

:Reset Value: 0xc

:Description: reg4 is a very usefull register. It can take down the moon when configured correctly.

+------------+---------------+----------+--------------------+
|Bits        |Field name     |Type      |Description         +
+============+===============+==========+====================+
|[31:0]      |reg4           |          |                    +
+------------+---------------+----------+--------------------+

