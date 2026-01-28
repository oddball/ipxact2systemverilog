"""
Base types for the generated code are declared here, as well as exceptions and other supporting classes.
Functionality to read, write and modify registers is also provided here. Several methods are provided, all sharing the same
interface.
"""


class OutOfRangeReading(Exception):
    """Exception thrown when an out of range value is read from the register."""
    pass


class OutOfRangeWriting(Exception):
    """Exception thrown when an out of range value is attempted to be written to the register."""
    pass


class OutOfRangeSpecifying(Exception):
    """Exception thrown when an a boundary is specified that is incoherent (e.g. with the number of bits in a field)."""
    pass


class FieldNotWritable(Exception):
    """Exception thrown when attempting to write to a read-only field."""
    pass


class accesLayer:
    """This interface contains method declarations that should be used by classes that can implement any type of memory
     access the registers (including simulated). """
    def read_register(self, addr, offset=0, width=32):
        """
        Reads a register
        :param addr: address
        :param offset: bit offset
        :param width: number of bits after the offset to read
        :return: the requested bits from the register
        """
        raise NotImplementedError()

    def modify_register(self, addr, data, offset=0, width=32):
        """
        Partially writes a register
        :param addr: address
        :param addr: data to be written
        :param offset: bit offset
        :param width: number of bits after the offset to write
        """
        raise NotImplementedError()

    def write_register(self, addr, data):
        """
        writes a complete register
        :param addr: address
        :param addr: data to be written
        """
        raise NotImplementedError()


class IP():
    def __init__(self, parent, base_address, acces_layer=accesLayer):
        self._base_address = base_address
        self._parent = parent
        self._acces_layer = acces_layer

    def get_base_address(self):
        return self._base_address

    def get_acces_layer(self):
        return self._acces_layer


class Register():
    def __init__(self, parent_ip, address_offset):
        """
        Constructor for a register of an IP
        :param parent_ip: an IP object to which this register belongs
        :param address_offset: the address offset (from the IP's base address)
        """
        self._parent_ip = parent_ip
        self._address_offset = address_offset
        self._acces_layer = parent_ip.get_acces_layer()

    def get_address_offset(self):
        """
        Returns the address offset
        :return: the address offset
        """
        return self._address_offset

    def get_parent_ip(self):
        """
        Returns the parent IP object
        :return: the parent IP object
        """
        return self._parent_ip

    def get_acces_layer(self):
        """
        Returns the acces layer object currently used. Usually it's the parent IP's access layer
        :return: the acces layer object currently used
        """
        return self._acces_layer

    def get(self):
        """
        returns the value of this register (as unsigned int)
        :return: the value of this register
        """
        self.get_acces_layer().read_register(self.get_parent_ip().get_base_address() +
                                             self.get_address_offset())

    def set(self, value):
        """
        Sets the value of this register (as unsigned int)
        :value: the value to set this register
        """
        self.get_acces_layer().write_register(self.get_parent_ip().get_base_address() +
                                              self.get_address_offset(), value)


class Field():
    """This base class represents a field in the register. It will work like an unsigned integer field and is the prefered
        way of obtaining 'raw values' from the registers but should be derived from and not instanced. """
    def __init__(self, parent_register, bit_width, bit_offset, access):
        """
        Constructor for a Field of a register
        :param parent_register: parent register
        :param bit_width: number of bits used by the field
        :param bit_offset: bit offset from the beginning of the register
        :param acces: a string for accessibility ('read-write' / 'read-only')
        """
        self._parent_register = parent_register
        self._bit_width = bit_width
        self._bit_offset = bit_offset
        self._access = access

    def get(self):
        """
        Returns the value of the field
        :return: value of the field
        """
        return self._parent_register.get_acces_layer().read_register(self._parent_register.get_parent_ip().get_base_address() +
                                                                     self._parent_register.get_address_offset(),
                                                                     self._bit_offset,
                                                                     self._bit_width)

    def set(self, value):
        """
        Sets the value of the field
        :value: value to be set
        """
        if self._access == "read-only":
            raise FieldNotWritable()

        self._parent_register.get_acces_layer().modify_register(self._parent_register.get_parent_ip().get_base_address() +
                                                                self._parent_register.get_address_offset(),
                                                                value,
                                                                self._bit_offset,
                                                                self._bit_width)


class EnumField(Field):
    """Represents an enumerated type."""
    def __init__(self, parent_register, bit_width, bit_offset, access, enum_type):
        """
        :param name: name
        :param parent_register: parent register
        :param bit_width: number of bits used by the field
        :param bit_offset: bit offset from the beginning of the register
        :param acces: a string for accessibility ('read-write' / 'read-only')
        :param enum_type: a Python type derived from IntEnum which we want to represent
        """
        super().__init__(parent_register, bit_width, bit_offset, access)
        self._enum_type = enum_type
        self._int_values = list(map(int, enum_type))

    def get(self):
        """
        Returns the value of the field
        :return: the current enumeration represented by the field
        """
        val = super().get()
        if val not in self._int_values:
            return OutOfRangeReading()
        return self._enum_type(val)

    def set(self, value):
        """
         Sets the value of the field
         :value: value to be set. Either an integer or an enumeration of 'our' enumerated type
         """
        if value in self._int_values:
            super().set(value)
        else:
            raise OutOfRangeWriting()


class IntegerField(Field):
    """This class represents an (unsigned) integer. It derives from Field and relies on it for abstracting reads and
    writes. Therefore, this class is basically concerned with boundary checking."""
    def __init__(self, parent_register, bit_width, bit_offset, access, minimum, maximum):
        """
        Constructor for a Field of a register
        :param name: name
        :param parent_register: parent register
        :param bit_width: number of bits used by the field
        :param bit_offset: bit offset from the beginning of the register
        :param acces: a string for accessibility ('read-write' / 'read-only')
        :param minimum: minimum value that this field can have (None to assume the minimum representable)
        :param maximum: maximum value that this field can have (None to assume the maximum representable)
        """
        super().__init__(parent_register, bit_width, bit_offset, access)
        type_minimum = 0
        type_maximum = (2 ** bit_width) - 1
        if minimum is not None:
            if minimum < type_minimum:
                raise OutOfRangeSpecifying()
            else:
                self._minimum = minimum
        else:
            self._minimum = type_minimum

        if maximum is not None:
            if maximum > type_maximum:
                raise OutOfRangeSpecifying()
            else:
                self._maximum = maximum
        else:
            self._maximum = type_maximum

    def get(self):
        """
        Returns the value of the field
        :return: value of the field
        """
        val = super().get()
        if val < self._minimum or val > self._maximum:
            raise OutOfRangeReading()
        return val

    def set(self, value):
        """
        Sets the value of the field
        :value: value to be set
        """
        if value < self._minimum or value > self._maximum:
            raise OutOfRangeWriting()
        else:
            super().set(value)

    def get_minimum(self):
        """
        Gets the minimum value that can be defined for the field
        :return: minimum
        """
        return self._minimum

    def get_maximum(self):
        """
        Gets the maximum value that can be defined for the field
        :return: maximum
        """
        return self._maximum
