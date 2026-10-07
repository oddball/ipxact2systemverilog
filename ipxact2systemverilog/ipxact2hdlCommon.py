#!/usr/bin/env python3

# This file is part of ipxact2systemverilog
# Copyright (C) 2013 Andreas Lindh
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# andreas.lindh (a) hiced.com

import io
import json
import math
import os
import sys
import xml.etree.ElementTree as ETree

from mdutils.mdutils import MdUtils
from rstcloth import RstCloth

from .validate import ipxact_namespace, resolve_ipxact_version

DEFAULT_INI = {
    "global": {"unusedholes": "yes", "onebitenum": "no"},
    "vhdl": {"PublicConvFunct": "no", "std": "unresolved"},
    "rst": {"sphinx": "no", "wavedrom": "no"},
    "py": {"imports": "absolute"},
}


def sort_register_and_fill_holes(
    reg_name,
    field_name_list,
    bit_offset_list,
    bit_width_list,
    field_desc_list,
    enum_type_list,
    field_maximum_list,
    field_minimum_list,
    size,
    unused_holes=True,
):
    # sort the lists, highest offset first
    bit_offset_list = [int(x) for x in bit_offset_list]
    bit_width_list = [int(x) for x in bit_width_list]
    matrix = list(zip(bit_offset_list, field_name_list, bit_width_list, field_desc_list, enum_type_list, field_maximum_list, field_minimum_list))
    matrix.sort(key=lambda x: x[0])
    bit_offset_list, field_name_list, bit_width_list, field_desc_list, enum_type_list, field_maximum_list, field_minimum_list = list(zip(*matrix))
    # zip return tuples not lists
    field_name_list = list(field_name_list)
    bit_offset_list = list([int(x) for x in bit_offset_list])
    bit_width_list = list([int(x) for x in bit_width_list])
    field_desc_list = list(field_desc_list)
    enum_type_list = list(enum_type_list)
    field_maximum_list = list(field_maximum_list)
    field_minimum_list = list(field_minimum_list)

    if unused_holes:
        un_used_cnt = 0
        next_field_starting_pos = 0
        # fill up the holes
        index = 0
        register_width = bit_offset_list[-1] + bit_width_list[-1]
        while register_width > next_field_starting_pos:
            if next_field_starting_pos != bit_offset_list[index]:
                new_bit_width = bit_offset_list[index] - next_field_starting_pos
                bit_offset_list.insert(index, next_field_starting_pos)
                field_name_list.insert(index, "unused" + str(un_used_cnt))
                bit_width_list.insert(index, new_bit_width)
                field_desc_list.insert(index, "unused")
                enum_type_list.insert(index, "")
                field_maximum_list.insert(index, None)
                field_minimum_list.insert(index, None)
                un_used_cnt += 1
            next_field_starting_pos = int(bit_offset_list[index]) + int(bit_width_list[index])
            index += 1
        if next_field_starting_pos < size:
            bit_offset_list.insert(index, next_field_starting_pos)
            field_name_list.insert(index, "unused" + str(un_used_cnt))
            bit_width_list.insert(index, size - next_field_starting_pos)
            field_desc_list.insert(index, "unused")
            field_maximum_list.insert(index, None)
            field_minimum_list.insert(index, None)
            enum_type_list.insert(index, "")

    return reg_name, field_name_list, bit_offset_list, bit_width_list, field_desc_list, enum_type_list, field_maximum_list, field_minimum_list


class DocumentClass:
    def __init__(self, name):
        self.name = name
        self.memory_map_list = []

    def add_memory_map(self, memory_map):
        self.memory_map_list.append(memory_map)


class MemoryMapClass:
    def __init__(self, name):
        self.name = name
        self.address_block_list = []

    def add_address_block(self, address_block):
        self.address_block_list.append(address_block)


class AddressBlockClass:
    def __init__(self, name, description, base_address, addr_width, data_width):
        self.name = name
        self.description = description
        self.base_address = base_address
        self.addr_width = addr_width
        self.data_width = data_width
        self.register_list = []
        self.suffix = ""

    def add_register(self, reg):
        assert isinstance(reg, RegisterClass)
        self.register_list.append(reg)

    def set_register_list(self, register_list):
        self.register_list = register_list

    def return_as_string(self):
        raise NotImplementedError("method return_as_string() is virutal and must be overridden.")


class RegisterClass:
    def __init__(
        self,
        name,
        address,
        reset_value,
        size,
        access,
        desc,
        field_name_list,
        bit_offset_list,
        bit_width_list,
        field_desc_list,
        enum_type_list,
        field_maximum_constraints_list,
        field_minimum_constraints_list,
    ):
        assert isinstance(enum_type_list, list), "enumTypeList is not a list"
        self.name = name
        self.address = address
        self.reset_value = reset_value
        self.size = size
        self.access = access
        self.desc = desc
        self.field_name_list = field_name_list
        self.bit_offset_list = bit_offset_list
        self.bit_width_list = bit_width_list
        self.field_desc_list = field_desc_list
        self.enum_type_list = enum_type_list
        self.field_maximum_constraints_list = field_maximum_constraints_list
        self.field_minimum_constraints_list = field_minimum_constraints_list


class EnumTypeClassRegistry:
    """should perhaps be a singleton instead"""

    def __init__(self):
        self.list_of_enums = []

    def enum_all_ready_exist(self, enum):
        for e in self.list_of_enums:
            if e.compare(enum):
                enum.all_ready_exist = True
                enum.enum_name = e.name
                break
        self.list_of_enums.append(enum)
        return enum


class EnumTypeClass:
    def __init__(self, name, bit_width, key_list, value_list, descr_list):
        self.name = name
        self.bit_width = bit_width
        matrix = list(zip(value_list, key_list, descr_list))
        matrix.sort(key=lambda x: x[0])
        value_list, key_list, descr_list = list(zip(*matrix))
        self.key_list = list(key_list)
        self.value_list = list(value_list)
        self.all_ready_exist = False
        self.enum_name = None
        self.descr_list = descr_list

    def compare(self, other):
        result = True
        result = self.bit_width == other.bit_width and result
        result = self.compare_lists(self.key_list, other.key_list) and result
        result = self.compare_lists(self.value_list, other.value_list) and result

        return result

    def compare_lists(self, list1, list2):
        return list1 == list2


class PyAddressBlock(AddressBlockClass):
    """Generates a Python file from a IP-XACT register description"""

    def __init__(self, name, description, base_address, addr_width, data_width, config):
        self.name = name
        self.description = description
        self.base_address = base_address
        self.addr_width = addr_width
        self.data_width = data_width
        self.register_list = []
        self.suffix = ".py"
        self.library = ""
        self.config = config
        if self.config["py"]["imports"] == "absolute":
            self.imports = "absolute"
        else:
            self.imports = "relative"

    def return_as_string(self):
        r = ""
        r += self.return_pkg_header_string()
        r += self.return_object_class()
        r += self.return_registers_class()
        r += self.return_ip_class()
        return r

    def return_include_string(self):
        lib_file = os.path.join(os.path.dirname(__file__), "ipxact2pyCommon" + self.suffix)
        f = open(lib_file, "r", encoding="utf-8")
        return f.read()

    def return_pkg_header_string(self):
        r = ""
        r += "# Automatically generated\n"
        r += f"# with the command '{' '.join(sys.argv)}'\n"
        r += "#\n"
        r += "# Do not manually edit!\n"
        r += "#\n"
        r += "\n"
        return r

    def return_object_class(self):
        r = ""
        r += "from enum import IntEnum\n\n"

        if self.imports == "absolute":
            r += "from acces_layer import *\n"
        else:
            r += "from .acces_layer import *\n"

        r += "\n\n"
        return r

    def return_registers_class(self):
        r = ""

        # Do for all registers
        for reg in self.register_list:
            for i, enum in enumerate(reg.enum_type_list):
                if enum:
                    r += f"# {reg.field_desc_list[i]}\n"
                    r += f"class {enum.name}_enum(IntEnum):\n"
                    for i in range(len(enum.key_list)):
                        r += f"    {enum.key_list[i]} = {enum.value_list[i]}"
                        if enum.descr_list[i]:
                            r += f"  # {enum.descr_list[i]}"

                        r += "\n"
                    r += "\n\n"

            r += f"class {reg.name}_type(Register):\n"
            if reg.desc:
                r += '    """\n'
                r += f"    {reg.desc}\n"
                r += '    """\n\n'

            # r += "    def __init__(self, parent_ip, address_offset):\n"
            r += "    def __init__(\n"
            r += "        self,\n"
            r += "        parent_ip: IP,\n"
            r += "        address_offset: int,\n"
            r += "    ):\n"
            # r += "        super().__init__(parent_ip, address_offset)\n"
            r += "        super().__init__(\n"
            r += "            parent_ip,\n"
            r += "            address_offset,\n"
            r += "        )"
            r += "\n"

            for i in list(range(len(reg.field_name_list))):
                bits = f"[{reg.bit_offset_list[i] + reg.bit_width_list[i] - 1}:{reg.bit_offset_list[i]}]"
                bit = f"[{reg.bit_offset_list[i]}]"
                if reg.bit_width_list[i] == 1:  # field with only one bit
                    r += f"        # {bit}\n"
                else:
                    r += f"        # {bits}\n"
                if reg.field_desc_list[i]:
                    desc_lines = reg.field_desc_list[i].split("\n")
                    for line in desc_lines:
                        r += f"        # {line}\n"
                if reg.enum_type_list[i]:
                    r += f"        self._{reg.field_name_list[i]} = EnumField(\n"
                    r += "            self,\n"
                    r += f"            bit_width={reg.bit_width_list[i]},\n"
                    r += f"            bit_offset={reg.bit_offset_list[i]},\n"
                    r += f'            access="{reg.access}",\n'
                    r += f"            enum_type={reg.enum_type_list[i].name}_enum,\n"
                    r += "        )"
                else:
                    r += f"        self._{reg.field_name_list[i]} = IntegerField(\n"
                    r += "            self,\n"
                    r += f"            bit_width={reg.bit_width_list[i]},\n"
                    r += f"            bit_offset={reg.bit_offset_list[i]},\n"
                    r += f'            access="{reg.access}",\n'
                    r += f"            minimum={reg.field_minimum_constraints_list[i]},\n"
                    r += f"            maximum={reg.field_maximum_constraints_list[i]},\n"
                    r += "        )"
                r += "\n"

            r += "\n"

            for i in list(range(len(reg.field_name_list))):
                r += "    @property\n"
                r += f"    def {reg.field_name_list[i]}(self):\n"
                r += f"        return self._{reg.field_name_list[i]}.get()\n"
                r += "\n"
                r += f"    @{reg.field_name_list[i]}.setter\n"
                if reg.enum_type_list[i]:
                    r += f"    def {reg.field_name_list[i]}(self, value: {reg.enum_type_list[i].name}_enum):\n"
                else:
                    r += f"    def {reg.field_name_list[i]}(self, value: int):\n"
                r += f"        self._{reg.field_name_list[i]}.set(value)\n"
                r += "\n"

            r += "\n"

        return r

    def return_ip_class(self):
        r = ""
        r += f"class {self.name}_type(IP):\n"
        r += "    def __init__(self, parent: IP, base_address=0, access_layer=accesLayer):\n"
        r += "        super().__init__(parent, base_address, access_layer)\n\n"
        # Do for all registers
        _width = math.ceil(self.addr_width / 4) + 2  # +2 for the '0x'
        for reg in self.register_list:
            r += f"        self.{reg.name} = {reg.name}_type(self, address_offset={reg.address:#0{_width}x})\n"

        return r


class RstAddressBlock(AddressBlockClass):
    """Generates a ReStructuredText file from a IP-XACT register description"""

    def __init__(self, name, description, base_address, addr_width, data_width, config):
        super().__init__(name, description, base_address, addr_width, data_width)
        self.suffix = ".rst"
        self.config = config

    def return_enum_value_string(self, enum_type_obj):
        if isinstance(enum_type_obj, EnumTypeClass):
            items = []
            for i in range(len(enum_type_obj.key_list)):
                items.append(enum_type_obj.key_list[i] + "=" + enum_type_obj.value_list[i])
            s = ", ".join(items)
        else:
            s = ""
        return s

    def return_as_string(self):
        r = RstCloth(io.StringIO())  # with default parameter, sys.stdout is used
        reg_name_list = [reg.name for reg in self.register_list]
        reg_address_list = [reg.address for reg in self.register_list]
        reg_descr_list = [reg.desc for reg in self.register_list]

        r.title(self.name)  # Use the name of the addressBlock as title
        r.newline()
        r.content(self.description)
        r.newline()
        r.field("Base Address", hex(self.base_address))
        r.newline()
        r.h2("Registers")

        summary_table = []
        for i in range(len(reg_name_list)):
            # only use sphinx extentions when generating RestructuredText for Sphinx
            if self.config["rst"].getboolean("sphinx"):
                _link = f":ref:`reg_{reg_name_list[i]}`"
            else:
                _link = f"{reg_name_list[i]}_"
            summary_table.append(["%#04x" % reg_address_list[i], _link, str(reg_descr_list[i])])
        r.table(header=["Address", "Register Name", "Description"], data=summary_table)

        for reg in self.register_list:
            r.ref_target(name=f"reg_{reg.name}")
            r.newline()
            r.h2(reg.name)
            r.newline()
            r.field("Name", reg.name)
            r.field("Address", hex(reg.address))
            if reg.reset_value:
                # display the resetvalue in hex notation in the full length of the register
                r.field("Reset Value", "{value:#0{size:d}x}".format(value=int(reg.reset_value, 0), size=reg.size // 4 + 2))
            r.field("Access", reg.access)
            r.field("Description", reg.desc)

            reg_table = []
            for field_index in reversed(list(range(len(reg.field_name_list)))):
                if reg.bit_width_list[field_index] == 1:  # only one bit -> no range needed
                    bits = f"{reg.bit_offset_list[field_index]}"
                else:
                    bits = f"[{reg.bit_offset_list[field_index] + reg.bit_width_list[field_index] - 1}:{reg.bit_offset_list[field_index]}]"
                _line = [bits, reg.field_name_list[field_index]]

                if reg.reset_value:
                    temp = int(reg.reset_value, 0) >> reg.bit_offset_list[field_index]
                    mask = (2 ** reg.bit_width_list[field_index]) - 1
                    temp &= mask
                    temp = "{value:#0{width}x}".format(value=temp, width=math.ceil(reg.bit_width_list[field_index] / 4) + 2)
                    _line.append(temp)
                _line.append(reg.field_desc_list[field_index])
                reg_table.append(_line)

            _headers = ["Bits", "Field name"]
            if reg.reset_value:
                _headers.append("Reset")
            _headers.append("Description")

            # insert the wavedrom bitfield register (only when using Sphinx)
            if self.config["rst"].getboolean("wavedrom"):
                py = []

                i = 0
                field_index = 0
                while i < reg.size:
                    # search if bit i is the start of an defined register field
                    temp = [x for x in reg.bit_offset_list if x == i]
                    f = {}
                    if temp:  # yes, i is the start of an register field
                        f["name"] = reg.field_name_list[field_index]
                        f["bits"] = reg.bit_width_list[field_index]
                        if reg.reset_value:
                            temp = int(reg.reset_value, 0) >> i
                            mask = (2 ** f["bits"]) - 1
                            temp &= mask
                            f["attr"] = temp
                        i += reg.bit_width_list[field_index]  # next search position
                        field_index += 1
                    else:  # detected a gap in the register
                        # not f['name'] -> gray field with Wavedrom
                        try:
                            f["bits"] = 1
                            i += 1
                        except IndexError:  # no next field defined
                            f["bits"] = reg.size - i
                            i = reg.size
                        if reg.reset_value:
                            temp = int(reg.reset_value, 0) >> i
                            mask = (2 ** f["bits"]) - 1
                            temp &= mask
                            f["attr"] = temp

                    py.append(f)

                wd = {
                    "reg": py,
                    "config": {
                        "lanes": reg.size // 8,
                        "bits": reg.size,
                    },
                }
                r.newline()
                r.directive(name="wavedrom", fields=[("alt", reg.name)], content=json.dumps(wd, indent=1).splitlines())

            # table of the register
            r.table(header=_headers, data=reg_table)

            # enumerations
            for enum in reg.enum_type_list:
                if enum:
                    # header
                    r.ref_target(name=f"enum_{enum.name}")
                    r.newline()
                    r.h3(enum.name)
                    # table
                    enum_table = []
                    for i in range(len(enum.key_list)):
                        _value = "{value:#0{width}x}".format(value=int(enum.value_list[i], 0), width=math.ceil(int(enum.bit_width, 0) / 4) + 2)

                        _line = [enum.key_list[i], _value, enum.descr_list[i]]
                        enum_table.append(_line)
                    r.table(header=["Name", "Value", "Description"], data=enum_table)

            # constraints
            for field_index, (mini, maxi) in enumerate(zip(reg.field_minimum_constraints_list, reg.field_maximum_constraints_list)):
                if mini and maxi:
                    # header
                    r.h3(reg.field_name_list[field_index])
                    r.newline()
                    r.field("Minimum", "{value:#0{size:d}x}".format(value=int(mini), size=(reg.bit_width_list[field_index] // 4 + 2)))
                    r.field("Maximum", "{value:#0{size:d}x}".format(value=int(maxi), size=(reg.bit_width_list[field_index] // 4 + 2)))
                    r.newline()

        return r.data


class MdAddressBlock(AddressBlockClass):
    """Generates a Markdown file from a IP-XACT register description"""

    def __init__(self, name, description, base_address, addr_width, data_width, config):
        super().__init__(name, description, base_address, addr_width, data_width)
        self.suffix = ".md"
        self.md_file = MdUtils(file_name="none", title="")

    def return_enum_value_string(self, enum_type_obj):
        if isinstance(enum_type_obj, EnumTypeClass):
            items = []
            for i in range(len(enum_type_obj.key_list)):
                items.append(enum_type_obj.key_list[i] + "=" + enum_type_obj.value_list[i])
            s = ", ".join(items)
        else:
            s = ""
        return s

    def return_as_string(self):
        reg_name_list = [reg.name for reg in self.register_list]
        reg_address_list = [reg.address for reg in self.register_list]
        reg_descr_list = [reg.desc for reg in self.register_list]

        self.md_file.new_header(level=1, title=self.name)  # Use the name of the addressBlock as title
        self.md_file.new_paragraph(self.description)
        self.md_file.new_paragraph(f"Base Address: {self.base_address:#x}")
        self.md_file.new_paragraph()
        self.md_file.new_header(level=2, title="Registers")

        # summary
        header = ["Address", "Register Name", "Description"]
        rows = []
        for i in range(len(reg_name_list)):
            rows.extend(["{:#04x}".format(reg_address_list[i]), f"[{reg_name_list[i]}](#{reg_name_list[i]})", str(reg_descr_list[i])])
        self.md_file.new_table(
            columns=len(header),
            rows=len(reg_name_list) + 1,  # header + data
            text=header + rows,
            text_align="left",
        )

        # all registers
        for reg in self.register_list:
            headers = ["Bits", "Field name"]
            if reg.reset_value:
                headers.append("Reset")
            headers.append("Description")

            self.return_md_reg_desc(reg.name, reg.address, reg.size, reg.reset_value, reg.desc, reg.access)
            reg_table = []
            for field_index in reversed(list(range(len(reg.field_name_list)))):
                if reg.bit_width_list[field_index] == 1:  # only one bit -> no range needed
                    bits = f"{reg.bit_offset_list[field_index]}"
                else:
                    bits = f"[{reg.bit_offset_list[field_index] + reg.bit_width_list[field_index] - 1}:{reg.bit_offset_list[field_index]}]"
                reg_table.append(bits)
                reg_table.append(reg.field_name_list[field_index])
                if reg.reset_value:
                    temp = int(reg.reset_value, 0) >> reg.bit_offset_list[field_index]
                    mask = (2 ** reg.bit_width_list[field_index]) - 1
                    temp &= mask
                    temp = "{value:#0{width}x}".format(value=temp, width=math.ceil(reg.bit_width_list[field_index] / 4) + 2)
                    reg_table.append(temp)
                reg_table.append(reg.field_desc_list[field_index])

            self.md_file.new_table(columns=len(headers), rows=len(reg.field_name_list) + 1, text=headers + reg_table, text_align="left")

            # enumerations
            for enum in reg.enum_type_list:
                if enum:
                    self.md_file.new_header(level=4, title=enum.name)
                    enum_table = []
                    for i in range(len(enum.key_list)):
                        _value = "{value:#0{width}x}".format(value=int(enum.value_list[i], 0), width=math.ceil(int(enum.bit_width, 0) / 4) + 2)
                        enum_table.append(enum.key_list[i])
                        enum_table.append(_value)
                        enum_table.append(enum.descr_list[i])
                    headers = ["Name", "Value", "Description"]
                    self.md_file.new_table(columns=len(headers), rows=len(enum.key_list) + 1, text=headers + enum_table, text_align="left")

            # constraints
            for field_index, (mini, maxi) in enumerate(zip(reg.field_minimum_constraints_list, reg.field_maximum_constraints_list)):
                if mini and maxi:
                    # header
                    self.md_file.new_header(level=4, title=reg.field_name_list[field_index])
                    self.md_file.new_line("**Minimum** " + "{value:#0{size:d}x}".format(value=int(mini), size=(reg.bit_width_list[field_index] // 4 + 2)))
                    self.md_file.new_line("**Maximum** " + "{value:#0{size:d}x}".format(value=int(maxi), size=(reg.bit_width_list[field_index] // 4 + 2)))
                    self.md_file.new_line()

        return self.md_file.file_data_text

    def return_md_reg_desc(self, name, address, size, reset_value, desc, access):
        self.md_file.new_header(level=3, title=name)
        self.md_file.new_line("**Name** " + str(name))
        self.md_file.new_line("**Address** " + hex(address))
        if reset_value:
            # display the resetvalue in hex notation in the full length of the register
            self.md_file.new_line("**Reset Value** {value:#0{size:d}x}".format(value=int(reset_value, 0), size=size // 4 + 2))
        self.md_file.new_line("**Access** " + access)
        self.md_file.new_line("**Description** " + desc)


class VhdlAddressBlock(AddressBlockClass):
    """Generates a vhdl file from a IP-XACT register description"""

    def __init__(self, name, description, base_address, addr_width, data_width, config):
        super().__init__(name, description, base_address, addr_width, data_width)
        self.suffix = "_vhd_pkg.vhd"
        self.config = config
        if self.config["vhdl"]["std"] == "resolved":
            self.std = "std_logic"
            self.sulv = "slv"  # Std_Logic_Vector
        else:
            self.std = "std_ulogic"
            self.sulv = "sulv"  # Std_ULogic_Vector

    def has_write_registers(self):
        """Return True if the there are registers that can be written."""
        ret = False
        for reg in self.register_list:
            if reg.access == "read-write":
                ret = True
                break
        return ret

    def return_as_string(self):
        r = ""
        r += self.return_pkg_header_string()
        r += "\n\n"
        r += self.return_pkg_body_string()
        return r

    def return_pkg_header_string(self):
        r = ""
        r += "--\n"
        r += "-- Automatically generated\n"
        r += f"-- with the command '{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}'\n"
        r += "--\n"
        r += "-- Do not manually edit!\n"
        r += "--\n"
        r += "-- VHDL 93\n"
        r += "--\n"
        r += "\n"
        r += "library ieee;\n"
        r += "use ieee.std_logic_1164.all;\n"
        r += "use ieee.numeric_std.all;\n"
        r += "\n"
        r += f"package {self.name}_vhd_pkg is\n"
        r += "\n"
        r += f"  constant addr_width : natural := {self.addr_width};\n"
        r += f"  constant data_width : natural := {self.data_width};\n"

        r += "\n\n"

        r += self.return_reg_field_enum_type_strings(True)

        for reg in self.register_list:
            _width = math.ceil(self.addr_width / 4) + 2  # +2 for the '0x'
            r += f"  constant {reg.name}_addr : natural := {reg.address};  -- {reg.address:#0{_width}x}\n"
        r += "\n"

        for reg in self.register_list:
            if reg.reset_value:
                _value = int(reg.reset_value, 0)
                _width = math.ceil((self.data_width / 4)) + 2  # +2 for the '0x'
                r += f"  constant {reg.name}_reset_value : {self.std}_vector(data_width-1 downto 0) := {self.std}_vector(to_unsigned({_value:d}, data_width));  -- {_value:#0{_width}x}\n"
                # show reset value for every field
                for field_index in reversed(list(range(len(reg.field_name_list)))):
                    _name = reg.field_name_list[field_index]
                    _value = int(reg.reset_value, 0) >> reg.bit_offset_list[field_index]
                    mask = (2 ** reg.bit_width_list[field_index]) - 1
                    _value &= mask
                    _value = "{value:#0{width}x}".format(value=_value, width=math.ceil(reg.bit_width_list[field_index] / 4) + 2)
                    r += f"    -- {_name} = {_value}\n"

        r += "\n\n"

        for reg in self.register_list:
            r += self.return_reg_record_type_string(reg)

        r += self.return_registers_in_record_type_string()
        if self.has_write_registers():
            r += self.return_registers_out_record_type_string()
        r += self.return_registers_read_function()
        if self.has_write_registers():
            r += self.return_registers_write_function()
            r += self.return_registers_reset_function()

        if self.config["vhdl"].getboolean("PublicConvFunct"):
            for reg in self.register_list:
                r += self.return_rec_to_sulv_function(reg)
                r += self.return_sulv_to_rec_function(reg)

        r += "end;\n"

        return r

    def return_reg_field_enum_type_strings(self, prototype):
        r = ""
        for reg in self.register_list:
            for enum in reg.enum_type_list:
                if isinstance(enum, EnumTypeClass) and not enum.all_ready_exist:
                    r += f"  -- {enum.name}\n"  # group the enums in the package
                    if prototype:
                        t = f"  type {enum.name}_enum is ("
                        indent = t.find("(") + 1
                        r += t
                        for ki in range(len(enum.key_list)):
                            if ki != 0:  # no indentation for the first element
                                r += " " * indent
                            r += enum.key_list[ki]
                            if ki != len(enum.key_list) - 1:  # no ',' for the last element
                                r += ","
                            else:  # last element
                                r += ");"
                            if enum.descr_list[ki]:
                                r += f"  -- {enum.descr_list[ki]}"
                            if ki != len(enum.key_list) - 1:  # no new line for the last element
                                r += "\n"
                        r += "\n"

                    r += f"  function {enum.name}_enum_to_{self.sulv}(v: {enum.name}_enum) return {self.std}_vector"
                    if prototype:
                        r += ";\n"
                    else:
                        r += " is\n"
                        r += f"    variable r : {self.std}_vector({enum.bit_width}-1 downto 0);\n"
                        r += "  begin\n"
                        r += "       case v is\n"
                        for i in range(len(enum.key_list)):
                            r += '         when {key} => r:="{value_int:0{bitwidth}b}"; -- {value}\n'.format(
                                key=enum.key_list[i], value=enum.value_list[i], value_int=int(enum.value_list[i], 0), bitwidth=int(enum.bit_width, 0)
                            )
                        r += "       end case;\n"
                        r += "    return r;\n"
                        r += "  end function;\n\n"

                    r += f"  function {self.sulv}_to_{enum.name}_enum(v: {self.std}_vector({enum.bit_width}-1 downto 0)) return {enum.name}_enum"
                    if prototype:
                        r += ";\n"
                    else:
                        r += " is\n"
                        r += f"    variable r : {enum.name}_enum;\n"
                        r += "  begin\n"
                        r += "       case v is\n"
                        for i in range(len(enum.key_list)):
                            r += '         when "{value_int:0{bitwidth}b}" => r:={key};\n'.format(
                                key=enum.key_list[i], value_int=int(enum.value_list[i], 0), bitwidth=int(enum.bit_width, 0)
                            )
                        r += f"         when others => r:={enum.key_list[0]}; -- error\n"
                        r += "       end case;\n"
                        r += "    return r;\n"
                        r += "  end function;\n\n"

                    if prototype:
                        r += "\n"
        if prototype:
            r += "\n"
        return r

    def return_reg_record_type_string(self, reg):
        r = ""
        r += f"  type {reg.name}_record_type is record\n"
        for i, mini, maxi in zip(
            reversed(list(range(len(reg.field_name_list)))), reg.field_minimum_constraints_list[::-1], reg.field_maximum_constraints_list[::-1]
        ):
            bits = f"[{reg.bit_offset_list[i] + reg.bit_width_list[i] - 1}:{reg.bit_offset_list[i]}]"
            bit = f"[{reg.bit_offset_list[i]}]"
            if isinstance(reg.enum_type_list[i], EnumTypeClass):
                if not reg.enum_type_list[i].all_ready_exist:
                    r += f"    {reg.field_name_list[i]} : {reg.enum_type_list[i].name}_enum; -- {bits}\n"
                else:
                    r += f"    {reg.field_name_list[i]} : {reg.enum_type_list[i].enum_name}_enum; -- {bits}\n"
            else:
                if reg.bit_width_list[i] == 1:  # single bit
                    r += f"    {reg.field_name_list[i]} : {self.std}; -- {bit}\n"
                else:  # vector
                    r += f"    {reg.field_name_list[i]} : {self.std}_vector({reg.bit_width_list[i] - 1} downto 0); -- {bits}"
                    if mini and maxi:
                        r += ", Min: " + "{value:#0{size:d}x}".format(value=int(mini), size=(reg.bit_width_list[-i] // 4 + 2))
                        r += ", Max: " + "{value:#0{size:d}x}".format(value=int(maxi), size=(reg.bit_width_list[-i] // 4 + 2))
                        r += "\n"
                    else:
                        r += "\n"
        r += "  end record;\n\n"
        return r

    def return_registers_in_record_type_string(self):
        r = ""
        r += f"  type {self.name}_in_record_type is record\n"
        for reg in self.register_list:
            if reg.access == "read-only":
                _width = math.ceil(self.addr_width / 4) + 2  # +2 for the '0x'
                r += f"    {reg.name} : {reg.name}_record_type; -- addr {reg.address:#0{_width}x}\n"
        r += "  end record;\n\n"
        return r

    def return_registers_out_record_type_string(self):
        r = ""
        r += f"  type {self.name}_out_record_type is record\n"
        for reg in self.register_list:
            if reg.access != "read-only":
                _width = math.ceil(self.addr_width / 4) + 2  # +2 for the '0x'
                r += f"    {reg.name} : {reg.name}_record_type; -- addr {reg.address:#0{_width}x}\n"
        r += "  end record;\n\n"
        return r

    def return_registers_read_function(self):
        r = f"  function read_{self.name}(registers_i : {self.name}_in_record_type;\n"
        indent = " " * (r.find("(") + 1)
        if self.has_write_registers():
            r += f"{indent}registers_o : {self.name}_out_record_type;\n"
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0)\n"
        r += f"{indent}) return {self.std}_vector;\n\n"
        return r

    def return_registers_write_function(self):
        r = f"  function write_{self.name}(value : {self.std}_vector(data_width-1 downto 0);\n"
        indent = " " * (r.find("(") + 1)
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0);\n"
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type;\n\n"
        return r

    def return_registers_reset_function(self):
        r = f"  function reset_{self.name} return {self.name}_out_record_type;\n"
        r += f"  function reset_{self.name}(address: {self.std}_vector(addr_width-1 downto 0);\n"
        indent = " " * (r.splitlines()[-1].find("(") + 1)
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type;\n\n"
        return r

    def return_rec_to_sulv_function_string(self, reg):
        r = ""
        r += f"  function {reg.name}_record_type_to_{self.sulv}(v : {reg.name}_record_type) return {self.std}_vector is\n"
        r += f"    variable r : {self.std}_vector(data_width-1 downto 0);\n"
        r += "  begin\n"
        r += "    r :=  (others => '0');\n"
        for i in reversed(list(range(len(reg.field_name_list)))):
            bits = f"{reg.bit_offset_list[i] + reg.bit_width_list[i] - 1} downto {reg.bit_offset_list[i]}"
            bit = str(reg.bit_offset_list[i])
            if isinstance(reg.enum_type_list[i], EnumTypeClass):
                if not reg.enum_type_list[i].all_ready_exist:
                    r += f"    r({bits}) := {reg.enum_type_list[i].name}_enum_to_{self.sulv}(v.{reg.field_name_list[i]});\n"
                else:
                    r += f"    r({bits}) := {reg.enum_type_list[i].enum_name}_enum_to_{self.sulv}(v.{reg.field_name_list[i]});\n"
            else:
                if reg.bit_width_list[i] == 1:  # single bit
                    r += f"    r({bit}) := v.{reg.field_name_list[i]};\n"
                else:  # vector
                    r += f"    r({bits}) := v.{reg.field_name_list[i]};\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def return_rec_to_sulv_function(self, reg):
        r = f"  function {reg.name}_record_type_to_{self.sulv}(v : {reg.name}_record_type) return {self.std}_vector;\n\n"
        return r

    def return_sulv_to_rec_function_string(self, reg):
        r = ""
        r += f"  function {self.sulv}_to_{reg.name}_record_type(v : {self.std}_vector) return {reg.name}_record_type is\n"
        r += f"    variable r : {reg.name}_record_type;\n"
        r += "  begin\n"
        for i in reversed(list(range(len(reg.field_name_list)))):
            bits = f"{reg.bit_offset_list[i] + reg.bit_width_list[i] - 1} downto {reg.bit_offset_list[i]}"
            bit = str(reg.bit_offset_list[i])
            if isinstance(reg.enum_type_list[i], EnumTypeClass):
                if not reg.enum_type_list[i].all_ready_exist:
                    r += f"    r.{reg.field_name_list[i]} := {self.sulv}_to_{reg.enum_type_list[i].name}_enum(v({bits}));\n"
                else:
                    r += f"    r.{reg.field_name_list[i]} := {self.sulv}_to_{reg.enum_type_list[i].enum_name}_enum(v({bits}));\n"
            else:
                if reg.bit_width_list[i] == 1:  # single bit
                    r += f"    r.{reg.field_name_list[i]} := v({bit});\n"
                else:
                    r += f"    r.{reg.field_name_list[i]} := v({bits});\n"
        r += "    return r;\n"
        r += "  end function;\n\n"

        return r

    def return_sulv_to_rec_function(self, reg):
        r = f"  function {self.sulv}_to_{reg.name}_record_type(v : {self.std}_vector) return {reg.name}_record_type;\n\n"
        return r

    def return_read_function_string(self):
        r = ""
        t = f"  function read_{self.name}(registers_i : {self.name}_in_record_type;\n"
        indent = " " * (t.find("(") + 1)
        r += t
        if self.has_write_registers():
            r += f"{indent}registers_o : {self.name}_out_record_type;\n"
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0)\n"
        r += f"{indent}) return {self.std}_vector is\n"
        r += f"    variable r : {self.std}_vector(data_width-1 downto 0);\n"
        r += "  begin\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.register_list:
            if reg.access == "read-only":
                r += f"      when {reg.name}_addr => r:= {reg.name}_record_type_to_{self.sulv}(registers_i.{reg.name});\n"
            else:
                r += f"      when {reg.name}_addr => r:= {reg.name}_record_type_to_{self.sulv}(registers_o.{reg.name});\n"
        r += "      when others => r := (others => '0');\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def return_write_function_string(self):
        r = ""
        t = f"  function write_{self.name}(value : {self.std}_vector(data_width-1 downto 0);\n"
        r += t
        indent = " " * (t.find("(") + 1)
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0);\n"
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        r += "    r := registers_o;\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.register_list:
            if reg.access != "read-only":
                r += f"         when {reg.name}_addr => r.{reg.name} := {self.sulv}_to_{reg.name}_record_type(value);\n"
        r += "      when others => null;\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def return_reset_function_string(self):
        r = ""
        r += f"  function reset_{self.name} return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        for reg in self.register_list:
            if reg.reset_value:
                if reg.access != "read-only":
                    r += f"         r.{reg.name} := {self.sulv}_to_{reg.name}_record_type({reg.name}_reset_value);\n"
        r += "    return r;\n"
        r += "  end function;\n"
        r += "\n"
        r += f"  function reset_{self.name}(address: {self.std}_vector(addr_width-1 downto 0);\n"
        indent = " " * (r.splitlines()[-1].find("(") + 1)
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        r += "    r := registers_o;\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.register_list:
            if reg.reset_value:
                if reg.access != "read-only":
                    r += f"         when {reg.name}_addr => r.{reg.name} := {self.sulv}_to_{reg.name}_record_type({reg.name}_reset_value);\n"
        r += "      when others => null;\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def return_pkg_body_string(self):
        r = ""
        r += f"package body {self.name}_vhd_pkg is\n\n"

        r += self.return_reg_field_enum_type_strings(False)

        for reg in self.register_list:
            r += self.return_rec_to_sulv_function_string(reg)
            r += self.return_sulv_to_rec_function_string(reg)

        r += self.return_read_function_string()
        if self.has_write_registers():
            r += self.return_write_function_string()
            r += self.return_reset_function_string()
        r += "end package body;\n"
        return r


class SystemVerilogAddressBlock(AddressBlockClass):
    def __init__(self, name, description, base_address, addr_width, data_width, config):
        super().__init__(name, description, base_address, addr_width, data_width)
        self.suffix = "_sv_pkg.sv"
        self.config = config

    def return_include_string(self):
        r = "\n"
        r += "`define " + self.name + "_addr_width " + str(self.addr_width) + "\n"
        r += "`define " + self.name + "_data_width " + str(self.data_width) + "\n"
        return r

    def return_size_string(self):
        r = "\n"
        r += "const int addr_width = " + str(self.addr_width) + ";\n"
        r += "const int data_width = " + str(self.data_width) + ";\n"
        return r

    def return_addresses_string(self):
        r = "\n"
        for reg in self.register_list:
            r += "const int " + reg.name + "_addr = " + str(reg.address) + ";\n"
        r += "\n"
        return r

    def return_address_list_string(self):
        r = "\n"
        r = "//synopsys translate_off\n"
        r += "const int " + self.name + "_regAddresses [" + str(len(self.register_list)) + "] = '{"
        items = []
        for reg in self.register_list:
            items.append("\n     " + reg.name + "_addr")

        r += ",".join(items)
        r += "};\n"
        r += "\n"
        r += "const string " + self.name + "_regNames [" + str(len(self.register_list)) + "] = '{"
        items = []
        for reg in self.register_list:
            items.append('\n      "' + reg.name + '"')
        r += ",".join(items)
        r += "};\n"

        r += "const reg " + self.name + "_regUnResetedAddresses [" + str(len(self.register_list)) + "] = '{"
        items = []
        for reg in self.register_list:
            if reg.reset_value:
                items.append("\n   1'b0")
            else:
                items.append("\n   1'b1")
        r += ",".join(items)
        r += "};\n"
        r += "\n"
        r += "//synopsys translate_on\n\n"
        return r

    def enumerated_type(self, prepend, field_name, value_names, values):
        r = "\n"
        members = []
        # dont want to create to simple names in the global names space.
        # should preppend with name from ipxact file
        for index in range(len(value_names)):
            name = value_names[index]
            value = values[index]
            members.append(name + "=" + value)
        r += "typedef enum { " + ",".join(members) + "} enum_" + field_name + ";\n"
        return r

    def return_reset_values_string(self):
        r = ""
        for reg in self.register_list:
            if reg.reset_value:
                r += "const " + reg.name + "_struct_type " + reg.name + "_reset_value = " + str(int(reg.reset_value, 0)) + ";\n"
        r += "\n"
        return r

    def return_struct_string(self):
        r = "\n"
        for reg in self.register_list:
            r += "\ntypedef struct packed {\n"
            for i, mini, maxi in zip(
                reversed(list(range(len(reg.field_name_list)))), reg.field_minimum_constraints_list[::-1], reg.field_maximum_constraints_list[::-1]
            ):
                bits = "bits [" + str(reg.bit_offset_list[i] + reg.bit_width_list[i] - 1) + ":" + str(reg.bit_offset_list[i]) + "]"
                if mini and maxi:
                    constraints = ", Min: " + "{value:#0{size:d}x}".format(value=int(mini), size=(reg.bit_width_list[-i] // 4 + 2))
                    constraints += ", Max: " + "{value:#0{size:d}x}".format(value=int(maxi), size=(reg.bit_width_list[-i] // 4 + 2))
                    constraints += "\n"
                else:
                    constraints = "\n"
                r += "   bit [" + str(reg.bit_width_list[i] - 1) + ":0] " + str(reg.field_name_list[i]) + ";//" + bits + constraints
            r += "} " + reg.name + "_struct_type;\n\n"
        return r

    def return_registers_struct_string(self):
        r = "typedef struct packed {\n"
        for reg in self.register_list:
            r += "   " + reg.name + "_struct_type " + reg.name + ";\n"
        r += "} " + self.name + "_struct_type;\n\n"
        return r

    def return_read_function_string(self):
        r = "function bit [31:0] read_" + self.name + "(" + self.name + "_struct_type registers,int address);\n"
        r += "      bit [31:0]  r;\n"
        r += "      case(address)\n"
        for reg in self.register_list:
            r += "         " + reg.name + "_addr: r[$bits(registers." + reg.name + ")-1:0] = registers." + reg.name + ";\n"
        r += "        default: r =0;\n"
        r += "      endcase\n"
        r += "      return r;\n"
        r += "endfunction\n\n"
        return r

    def return_write_function_string(self):
        t = "function " + self.name + "_struct_type write_" + self.name + "(bit [31:0] data, int address,\n"
        r = t
        indent = r.find("(") + 1
        r += " " * indent + self.name + "_struct_type registers);\n"
        r += "   " + self.name + "_struct_type r;\n"
        r += "   r = registers;\n"
        r += "   case(address)\n"
        for reg in self.register_list:
            r += "         " + reg.name + "_addr: r." + reg.name + " = data[$bits(registers." + reg.name + ")-1:0];\n"
        r += "   endcase // case address\n"
        r += "   return r;\n"
        r += "endfunction\n\n"
        return r

    def return_reset_function_string(self):
        r = "function " + self.name + "_struct_type reset_" + self.name + "();\n"
        r += "   " + self.name + "_struct_type r;\n"
        for reg in self.register_list:
            if reg.reset_value:
                r += "   r." + reg.name + "=" + reg.name + "_reset_value;\n"
        r += "   return r;\n"
        r += "endfunction\n"
        r += "\n"
        return r

    def return_as_string(self):
        r = ""
        r += "// Automatically generated\n"
        r += f"// with the command '{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}'\n"
        r += "//\n"
        r += "// Do not manually edit!\n"
        r += "//\n"
        r += "package " + self.name + "_sv_pkg;\n\n"
        r += self.return_size_string()
        r += self.return_addresses_string()
        r += self.return_address_list_string()
        r += self.return_struct_string()
        r += self.return_reset_values_string()
        r += self.return_registers_struct_string()
        r += self.return_read_function_string()
        r += self.return_write_function_string()
        r += self.return_reset_function_string()
        r += "endpackage //" + self.name + "_sv_pkg\n"
        return r


class CAddressBlock(AddressBlockClass):
    def __init__(self, name, description, base_address, addr_width, data_width, config):
        super().__init__(name, description, base_address, addr_width, data_width)
        self.suffix = ".h"

    def register_offset_name(self, reg):
        return self.name.upper() + "_" + reg.name.upper() + "_OFFSET"

    def register_reset_name(self, reg):
        return self.name.upper() + "_" + reg.name.upper() + "_RESET"

    def get_field_mask_name(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_MASK"

    def get_field_shift_name(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_SHIFT"

    def get_macro_name(self, reg, fieldname):
        return "GET_" + self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper()

    def field_minimum_name(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_MIN"

    def field_maximum_name(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_MAX"

    def return_register_offsets(self):
        r = ""
        r += "// ------------------------------------------------\n"
        r += "//  Register offsets\n"
        r += "// ------------------------------------------------\n"
        for reg in self.register_list:
            addr_str = "0x%0.2X" % reg.address
            r += "#define " + self.register_offset_name(reg) + "\t" + addr_str + "\t// " + reg.desc + "\n"

        r += "\n\n"
        return r

    def return_register_bit_operators(self):
        r = ""

        for reg in self.register_list:
            r += "// ------------------------------------------------\n"
            r += "//  Bit operations for register " + reg.name + "\n"
            r += "// ------------------------------------------------\n"
            for i, mini, maxi in zip(list(range(len(reg.field_name_list))), reg.field_minimum_constraints_list, reg.field_maximum_constraints_list):
                fieldname = reg.field_name_list[i]
                r += "#define " + self.get_field_shift_name(reg, fieldname) + "\t" + str(reg.bit_offset_list[i]) + "\n"
                mask = 2 ** reg.bit_width_list[i] - 1
                mask_str = "0x%0.2X" % mask
                r += "#define " + self.get_field_mask_name(reg, fieldname) + " \t" + mask_str + "\n"

                if mini and maxi:
                    r += (
                        "#define "
                        + self.field_minimum_name(reg, fieldname)
                        + " \t"
                        + "{value:#0{size:d}x}".format(value=int(mini), size=(reg.bit_width_list[i] // 4 + 2))
                        + "\n"
                    )
                    r += (
                        "#define "
                        + self.field_maximum_name(reg, fieldname)
                        + " \t"
                        + "{value:#0{size:d}x}".format(value=int(maxi), size=(reg.bit_width_list[i] // 4 + 2))
                        + "\n"
                    )

                r += "\n"

        return r

    def return_macros_functions(self):
        r = ""

        for reg in self.register_list:
            r += "\n"
            r += "// ------------------------------------------------\n"
            r += "//  Macro functions for register " + reg.name + "\n"
            for i in list(range(len(reg.field_name_list))):
                fieldname = reg.field_name_list[i]
                items = f"//  - {self.get_macro_name(reg, fieldname)} : {reg.field_desc_list[i]}"
                items = items.strip()  # avoid a space at the end of the line if field description is empty
                r += items + "\n"
            r += "// ------------------------------------------------\n"
            r += "\n"
            for fieldname in reg.field_name_list:
                operation = "((a >> " + self.get_field_shift_name(reg, fieldname) + ") & " + self.get_field_mask_name(reg, fieldname) + ")"

                r += "#define " + self.get_macro_name(reg, fieldname) + "(a)\t" + operation + "\n"

        return r

    def return_as_string(self):
        r = ""
        r += "#pragma once\n"
        r += "/* Automatically generated\n"
        r += f" *  with the command '{os.path.basename(sys.argv[0])} {' '.join(sys.argv[1:])}'\n"
        r += " *\n"
        r += " * Do not manually edit!\n"
        r += " *\n"
        r += " * Example usage:\n"
        r += " *     uint32_t datareg0 = read(dev, EXAMPLE_REG_ADDRESS_REG0);\n"
        r += " *\n"
        r += " *     uint8_t byte0 = (uint8_t)GET_EXAMPLE_REG0_BYTE0(datareg0);\n"
        r += " *     uint8_t byte1 = (uint8_t)GET_EXAMPLE_REG0_BYTE1(datareg0);\n"
        r += " *     uint8_t byte2 = (uint8_t)GET_EXAMPLE_REG0_BYTE2(datareg0);\n"
        r += " *     uint8_t byte3 = (uint8_t)GET_EXAMPLE_REG0_BYTE3(datareg0);\n"
        r += " *\n"
        r += " *\n"
        r += " *     uint32_t datareg7 = read(dev, EXAMPLE_REG_ADDRESS_REG7);\n"
        r += " *\n"
        r += " *     uint8_t nibble0 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE0(datareg7);\n"
        r += " *     uint8_t nibble1 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE1(datareg7);\n"
        r += " *     uint8_t nibble2 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE2(datareg7);\n"
        r += " */\n"

        r += self.return_register_offsets()
        r += self.return_register_bit_operators()
        r += self.return_macros_functions()

        r += "\n"
        r += "// End of " + self.name + self.suffix + "\n"
        return r


class IpxactParser:
    def __init__(self, src_file, config, xml_version=None):
        self.src_file = src_file
        self.config = config
        self.xml_version = xml_version
        self.enum_type_class_registry = EnumTypeClassRegistry()

    def return_document(self):
        tree = ETree.parse(self.src_file)
        self.xml_version = resolve_ipxact_version(tree, self.xml_version)
        namespace_uri = ipxact_namespace(self.xml_version)
        prefix = "ipxact" if self.xml_version == "2022" else "spirit"
        ETree.register_namespace(prefix, namespace_uri)
        ns = "{" + namespace_uri + "}"
        doc_name = tree.find(ns + "name").text
        d = DocumentClass(doc_name)
        memory_maps = tree.find(ns + "memoryMaps")
        memory_map_list = memory_maps.findall(ns + "memoryMap") if memory_maps is not None else []
        for memory_map in memory_map_list:
            memory_map_name = memory_map.find(ns + "name").text
            address_block_list = memory_map.findall(ns + "addressBlock")
            m = MemoryMapClass(memory_map_name)
            for address_block in address_block_list:
                # check first whether there is a description field
                if address_block.find(ns + "description") is not None:
                    description = address_block.find(ns + "description").text
                else:
                    description = ""
                address_block_name = address_block.find(ns + "name").text
                register_list = address_block.findall(ns + "register")
                base_address = int(address_block.find(ns + "baseAddress").text, 0)
                nbr_of_addresses = int(address_block.find(ns + "range").text, 0)  # TODO, this is wrong
                addr_width = int(math.ceil((math.log(base_address + nbr_of_addresses, 2))))
                data_width = int(address_block.find(ns + "width").text, 0)
                a = AddressBlockClass(address_block_name, description, base_address, addr_width, data_width)
                for register_elem in register_list:
                    reset_value = self._register_reset(ns, register_elem)
                    size = int(register_elem.find(ns + "size").text, 0)
                    access = self._register_access(ns, register_elem)
                    if register_elem.find(ns + "description") is not None:
                        desc = register_elem.find(ns + "description").text
                    else:
                        desc = ""
                    reg_address = base_address + int(register_elem.find(ns + "addressOffset").text, 0)
                    r = self.return_register(ns, register_elem, reg_address, reset_value, size, access, desc, data_width)
                    a.add_register(r)
                m.add_address_block(a)
            d.add_memory_map(m)

        return d

    def _register_access(self, ns, register_elem):
        if self.xml_version == "1.5":
            return register_elem.find(ns + "access").text

        # 2022 moved register access under accessPolicies, and field access under fieldAccessPolicies.
        policies = register_elem.find(ns + "accessPolicies")
        if policies is not None:
            for policy in policies.findall(ns + "accessPolicy"):
                access = policy.find(ns + "access")
                if access is not None and access.text:
                    return access.text

        for field in register_elem.findall(ns + "field"):
            access = self._field_access(ns, field)
            if access:
                return access
        return "read-write"

    def _field_access(self, ns, field):
        policies = field.find(ns + "fieldAccessPolicies")
        if policies is None:
            return None
        for policy in policies.findall(ns + "fieldAccessPolicy"):
            access = policy.find(ns + "access")
            if access is not None and access.text:
                return access.text
        return None

    def _register_reset(self, ns, register_elem):
        if self.xml_version == "1.5":
            reset = register_elem.find(ns + "reset")
            if reset is not None:
                return reset.find(ns + "value").text
            return None

        # 2022 stores reset on each field. Fold those into one register value.
        combined = 0
        found = False
        for field in register_elem.findall(ns + "field"):
            resets = field.find(ns + "resets")
            if resets is None:
                continue
            reset = resets.find(ns + "reset")
            if reset is None:
                continue
            value = reset.find(ns + "value")
            if value is None or value.text is None:
                continue
            offset = int(field.find(ns + "bitOffset").text, 0)
            width = int(field.find(ns + "bitWidth").text, 0)
            combined |= (int(value.text, 0) & ((1 << width) - 1)) << offset
            found = True
        if not found:
            return None
        return str(combined)

    def _write_value_constraint(self, ns, field):
        policies = field.find(ns + "fieldAccessPolicies")
        if policies is None:
            return None
        for policy in policies.findall(ns + "fieldAccessPolicy"):
            constraint = policy.find(ns + "writeValueConstraint")
            if constraint is not None:
                return constraint
        return None

    def return_register(self, ns, register_elem, reg_address, reset_value, size, access, reg_desc, data_width):
        reg_name = register_elem.find(ns + "name").text
        field_list = register_elem.findall(ns + "field")
        field_name_list = [item.find(ns + "name").text for item in field_list]
        bit_offset_list = [item.find(ns + "bitOffset").text for item in field_list]
        bit_width_list = [item.find(ns + "bitWidth").text for item in field_list]
        field_desc_list = []
        field_maximum_list = []
        field_minimum_list = []
        enum_type_list = []

        for item in field_list:
            if self.xml_version == "2022":
                write_value_constraints = self._write_value_constraint(ns, item)
            else:
                write_value_constraints = item.find(ns + "writeValueConstraint")
            if write_value_constraints is not None:
                minimum = write_value_constraints.find(ns + "minimum")
                maximum = write_value_constraints.find(ns + "maximum")
                if minimum is not None and maximum is not None and minimum.text and maximum.text:
                    field_minimum_list.append(minimum.text)
                    field_maximum_list.append(maximum.text)
                else:
                    field_minimum_list.append(None)
                    field_maximum_list.append(None)
            else:
                field_minimum_list.append(None)
                field_maximum_list.append(None)

        for item in field_list:
            description = item.find(ns + "description")
            # handle no or an empty description
            if description is None:
                field_desc_list.append("")
            elif hasattr(description, "text"):
                if description.text:
                    field_desc_list.append(description.text)
                else:
                    field_desc_list.append("")
            else:
                field_desc_list.append("")
        enum_type_list = []
        for index in range(len(field_list)):
            field_elem = field_list[index]
            bit_width = bit_width_list[index]
            field_name = field_name_list[index]
            enumerated_values_elem = field_elem.find(ns + "enumeratedValues")
            if enumerated_values_elem is not None:
                enumerated_value_list = enumerated_values_elem.findall(ns + "enumeratedValue")
                values_name_list = [item.find(ns + "name").text for item in enumerated_value_list]
                descr_list = [
                    item.find(ns + "description").text if item.find(ns + "description") is not None else ""
                    for item in enumerated_value_list
                ]
                values_list = [item.find(ns + "value").text for item in enumerated_value_list]
                if len(values_name_list) > 0:
                    if int(bit_width) > 1:  # if the field of a enum is longer than 1 bit, always use enums
                        enum = EnumTypeClass(field_name, bit_width, values_name_list, values_list, descr_list)
                        enum = self.enum_type_class_registry.enum_all_ready_exist(enum)
                        enum_type_list.append(enum)
                    else:  # bit field of 1 bit
                        if self.config["global"].getboolean("onebitenum"):  # do create one bit enums
                            enum = EnumTypeClass(field_name, bit_width, values_name_list, values_list, descr_list)
                            enum = self.enum_type_class_registry.enum_all_ready_exist(enum)
                            enum_type_list.append(enum)
                        else:  # dont create enums of booleans because this only decreases readability
                            enum_type_list.append(None)
                else:
                    enum_type_list.append(None)
            else:
                enum_type_list.append(None)

        if len(field_name_list) == 0:
            field_name_list.append(reg_name)
            bit_offset_list.append(0)
            bit_width_list.append(data_width)
            field_desc_list.append("")
            enum_type_list.append(None)
            field_minimum_list.append(None)
            field_maximum_list.append(None)

        (reg_name, field_name_list, bit_offset_list, bit_width_list, field_desc_list, enum_type_list, field_maximum_list, field_minimum_list) = (
            sort_register_and_fill_holes(
                reg_name,
                field_name_list,
                bit_offset_list,
                bit_width_list,
                field_desc_list,
                enum_type_list,
                field_maximum_list,
                field_minimum_list,
                size,
                self.config["global"].getboolean("unusedholes"),
            )
        )

        reg = RegisterClass(
            reg_name,
            reg_address,
            reset_value,
            size,
            access,
            reg_desc,
            field_name_list,
            bit_offset_list,
            bit_width_list,
            field_desc_list,
            enum_type_list,
            field_maximum_list,
            field_minimum_list,
        )
        return reg


class Ipxact2OtherGenerator:
    def __init__(
        self,
        dest_dir,
        config,
        naming_scheme="addressBlockName",
    ):
        self.dest_dir = dest_dir
        self.naming_scheme = naming_scheme
        self.config = config

    def write(self, file_name, string):
        _dest = os.path.join(self.dest_dir, file_name)
        print("writing file " + _dest)

        if not os.path.exists(os.path.dirname(_dest)):
            os.makedirs(os.path.dirname(_dest))

        with open(_dest, "w", encoding="utf-8") as f:
            f.write(string)

    def generate(self, generator_class, document):
        self.document = document
        doc_name = document.name
        for memory_map in document.memory_map_list:
            map_name = memory_map.name
            for address_block in memory_map.address_block_list:
                block_name = address_block.name

                block = generator_class(
                    address_block.name,
                    address_block.description,
                    address_block.base_address,
                    address_block.addr_width,
                    address_block.data_width,
                    self.config,
                )

                block.set_register_list(address_block.register_list)
                s = block.return_as_string()
                if self.naming_scheme == "addressBlockName":
                    file_name = block_name + block.suffix
                else:
                    file_name = doc_name + "_" + map_name + "_" + block_name + block.suffix

                self.write(file_name, s)

                if generator_class == SystemVerilogAddressBlock:
                    include_file_name = file_name + "h"
                    include_string = block.return_include_string()
                    self.write(include_file_name, include_string)
                elif generator_class == PyAddressBlock:
                    include_file_name = "acces_layer" + ".py"
                    include_string = block.return_include_string()
                    self.write(include_file_name, include_string)
                    if block.imports == "relative":
                        self.write("__init__.py", "")
