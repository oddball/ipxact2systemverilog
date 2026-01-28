# Automatically generated
# with the command '/home/labgrid/Thomas_vreys/ipxact2systemverilog/.venv/bin/ipxact2py --srcFile example/input/test.xml --destDir example/output'
#
# Do not manually edit!
#

from enum import IntEnum

from acces_layer import *


class reg0_type(Register):
    """
    write something useful for reg0
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [7:0]
        # write something useful for field0
        self._byte0 = IntegerField(
            self,
            bit_width=8,
            bit_offset=0,
            access="read-write",
            minimum=0,
            maximum=7,
        )
        # [15:8]
        # write something useful for field1
        self._byte1 = IntegerField(
            self,
            bit_width=8,
            bit_offset=8,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [23:16]
        # write something useful for field2
        self._byte2 = IntegerField(
            self,
            bit_width=8,
            bit_offset=16,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [31:24]
        # write something useful for field3
        self._byte3 = IntegerField(
            self,
            bit_width=8,
            bit_offset=24,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def byte0(self):
        return self._byte0.get()

    @byte0.setter
    def byte0(self, value: int):
        self._byte0.set(value)

    @property
    def byte1(self):
        return self._byte1.get()

    @byte1.setter
    def byte1(self, value: int):
        self._byte1.set(value)

    @property
    def byte2(self):
        return self._byte2.get()

    @byte2.setter
    def byte2(self, value: int):
        self._byte2.set(value)

    @property
    def byte3(self):
        return self._byte3.get()

    @byte3.setter
    def byte3(self, value: int):
        self._byte3.set(value)


class reg1_type(Register):
    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [31:0]
        # write something useful for field0
        self._field0 = IntegerField(
            self,
            bit_width=32,
            bit_offset=0,
            access="read-write",
            minimum=4,
            maximum=20,
        )

    @property
    def field0(self):
        return self._field0.get()

    @field0.setter
    def field0(self, value: int):
        self._field0.set(value)


# which monkey
class monkey_enum(IntEnum):
    chimp = 0x0  # a monkey
    gorilla = 0x1
    phb = 0x2  # and another monkey


# which monkey
class monkey2_enum(IntEnum):
    chimp = 0
    gorilla = 1
    phb = 2


# which monkey
class monkey3_enum(IntEnum):
    phb = 0
    gorilla = 1
    chimp = 2


# which monkey
class monkey4_enum(IntEnum):
    chimp = 0
    gorilla = 1
    bonobo = 2


class reg2_type(Register):
    """
    write something useful for reg2
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [0]
        # write something useful for field power
        self._power = IntegerField(
            self,
            bit_width=1,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [1]
        # write something useful for field power2
        self._power2 = IntegerField(
            self,
            bit_width=1,
            bit_offset=1,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [3:2]
        # which monkey
        self._monkey = EnumField(
            self,
            bit_width=2,
            bit_offset=2,
            access="read-write",
            enum_type=monkey_enum,
        )
        # [5:4]
        # which monkey
        self._monkey2 = EnumField(
            self,
            bit_width=2,
            bit_offset=4,
            access="read-write",
            enum_type=monkey2_enum,
        )
        # [7:6]
        # which monkey
        self._monkey3 = EnumField(
            self,
            bit_width=2,
            bit_offset=6,
            access="read-write",
            enum_type=monkey3_enum,
        )
        # [9:8]
        # which monkey
        self._monkey4 = EnumField(
            self,
            bit_width=2,
            bit_offset=8,
            access="read-write",
            enum_type=monkey4_enum,
        )
        # [31:10]
        # unused
        self._unused0 = IntegerField(
            self,
            bit_width=22,
            bit_offset=10,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def power(self):
        return self._power.get()

    @power.setter
    def power(self, value: int):
        self._power.set(value)

    @property
    def power2(self):
        return self._power2.get()

    @power2.setter
    def power2(self, value: int):
        self._power2.set(value)

    @property
    def monkey(self):
        return self._monkey.get()

    @monkey.setter
    def monkey(self, value: monkey_enum):
        self._monkey.set(value)

    @property
    def monkey2(self):
        return self._monkey2.get()

    @monkey2.setter
    def monkey2(self, value: monkey2_enum):
        self._monkey2.set(value)

    @property
    def monkey3(self):
        return self._monkey3.get()

    @monkey3.setter
    def monkey3(self, value: monkey3_enum):
        self._monkey3.set(value)

    @property
    def monkey4(self):
        return self._monkey4.get()

    @monkey4.setter
    def monkey4(self, value: monkey4_enum):
        self._monkey4.set(value)

    @property
    def unused0(self):
        return self._unused0.get()

    @unused0.setter
    def unused0(self, value: int):
        self._unused0.set(value)


class reg3_type(Register):
    """
    write something useful for reg3
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [31:0]
        # write something useful for field0
        self._field0 = IntegerField(
            self,
            bit_width=32,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def field0(self):
        return self._field0.get()

    @field0.setter
    def field0(self, value: int):
        self._field0.set(value)


class reg4_type(Register):
    """
    reg4 is a very useful register. It can take down the moon when configured correctly.
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [31:0]
        self._reg4 = IntegerField(
            self,
            bit_width=32,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def reg4(self):
        return self._reg4.get()

    @reg4.setter
    def reg4(self, value: int):
        self._reg4.set(value)


class reg5_type(Register):
    """
    reg5 is as useful as reg4 but without a reset value defined.
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [31:0]
        self._reg5 = IntegerField(
            self,
            bit_width=32,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def reg5(self):
        return self._reg5.get()

    @reg5.setter
    def reg5(self, value: int):
        self._reg5.set(value)


class reg6_type(Register):
    """
    reg6 is a read only register.
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [31:0]
        self._reg6 = IntegerField(
            self,
            bit_width=32,
            bit_offset=0,
            access="read-only",
            minimum=None,
            maximum=None,
        )

    @property
    def reg6(self):
        return self._reg6.get()

    @reg6.setter
    def reg6(self, value: int):
        self._reg6.set(value)


class reg7_type(Register):
    """
    write something useful for reg7
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [3:0]
        # write something useful for nibble0
        self._nibble0 = IntegerField(
            self,
            bit_width=4,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [7:4]
        # unused
        self._unused0 = IntegerField(
            self,
            bit_width=4,
            bit_offset=4,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [11:8]
        self._nibble1 = IntegerField(
            self,
            bit_width=4,
            bit_offset=8,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [15:12]
        # unused
        self._unused1 = IntegerField(
            self,
            bit_width=4,
            bit_offset=12,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [19:16]
        # write something useful for nibble2
        self._nibble2 = IntegerField(
            self,
            bit_width=4,
            bit_offset=16,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [31:20]
        # unused
        self._unused2 = IntegerField(
            self,
            bit_width=12,
            bit_offset=20,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def nibble0(self):
        return self._nibble0.get()

    @nibble0.setter
    def nibble0(self, value: int):
        self._nibble0.set(value)

    @property
    def unused0(self):
        return self._unused0.get()

    @unused0.setter
    def unused0(self, value: int):
        self._unused0.set(value)

    @property
    def nibble1(self):
        return self._nibble1.get()

    @nibble1.setter
    def nibble1(self, value: int):
        self._nibble1.set(value)

    @property
    def unused1(self):
        return self._unused1.get()

    @unused1.setter
    def unused1(self, value: int):
        self._unused1.set(value)

    @property
    def nibble2(self):
        return self._nibble2.get()

    @nibble2.setter
    def nibble2(self, value: int):
        self._nibble2.set(value)

    @property
    def unused2(self):
        return self._unused2.get()

    @unused2.setter
    def unused2(self, value: int):
        self._unused2.set(value)


class reg8_type(Register):
    """
    register with empty and no descriptions of the fields
    """

    def __init__(
        self,
        parent_ip: IP,
        address_offset: int,
    ):
        super().__init__(
            parent_ip,
            address_offset,
        )
        # [3:0]
        self._nibble0 = IntegerField(
            self,
            bit_width=4,
            bit_offset=0,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [7:4]
        # unused
        self._unused0 = IntegerField(
            self,
            bit_width=4,
            bit_offset=4,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [11:8]
        self._nibble1 = IntegerField(
            self,
            bit_width=4,
            bit_offset=8,
            access="read-write",
            minimum=None,
            maximum=None,
        )
        # [31:12]
        # unused
        self._unused1 = IntegerField(
            self,
            bit_width=20,
            bit_offset=12,
            access="read-write",
            minimum=None,
            maximum=None,
        )

    @property
    def nibble0(self):
        return self._nibble0.get()

    @nibble0.setter
    def nibble0(self, value: int):
        self._nibble0.set(value)

    @property
    def unused0(self):
        return self._unused0.get()

    @unused0.setter
    def unused0(self, value: int):
        self._unused0.set(value)

    @property
    def nibble1(self):
        return self._nibble1.get()

    @nibble1.setter
    def nibble1(self, value: int):
        self._nibble1.set(value)

    @property
    def unused1(self):
        return self._unused1.get()

    @unused1.setter
    def unused1(self, value: int):
        self._unused1.set(value)


class example_type(IP):
    def __init__(self, parent: IP, base_address=0, access_layer=accesLayer):
        super().__init__(parent, base_address, access_layer)

        self.reg0 = reg0_type(self, address_offset=0x0)
        self.reg1 = reg1_type(self, address_offset=0x1)
        self.reg2 = reg2_type(self, address_offset=0x2)
        self.reg3 = reg3_type(self, address_offset=0x3)
        self.reg4 = reg4_type(self, address_offset=0x4)
        self.reg5 = reg5_type(self, address_offset=0x5)
        self.reg6 = reg6_type(self, address_offset=0x6)
        self.reg7 = reg7_type(self, address_offset=0x7)
        self.reg8 = reg8_type(self, address_offset=0x8)
