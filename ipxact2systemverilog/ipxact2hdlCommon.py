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
import math
import os
import sys
import xml.etree.ElementTree as ETree
from mdutils.mdutils import MdUtils
from rstcloth import RstCloth

DEFAULT_INI = {'global': {'unusedholes': 'yes',
                          'onebitenum': 'no'},
               'vhdl': {'PublicConvFunct': 'no',
                        'std': 'unresolved'}}


def sortRegisterAndFillHoles(regName,
                             fieldNameList,
                             bitOffsetList,
                             bitWidthList,
                             fieldDescList,
                             enumTypeList,
                             size,
                             unusedHoles=True):
    # sort the lists, highest offset first
    bitOffsetList = [int(x) for x in bitOffsetList]
    bitWidthList = [int(x) for x in bitWidthList]
    matrix = list(zip(bitOffsetList, fieldNameList, bitWidthList, fieldDescList, enumTypeList))
    matrix.sort(key=lambda x: x[0])  # , reverse=True)
    bitOffsetList, fieldNameList, bitWidthList, fieldDescList, enumTypeList = list(zip(*matrix))
    # zip return tuples not lists
    fieldNameList = list(fieldNameList)
    bitOffsetList = list([int(x) for x in bitOffsetList])
    bitWidthList = list([int(x) for x in bitWidthList])
    fieldDescList = list(fieldDescList)
    enumTypeList = list(enumTypeList)

    if unusedHoles:
        unUsedCnt = 0
        nextFieldStartingPos = 0
        # fill up the holes
        index = 0
        register_width = bitOffsetList[-1] + bitWidthList[-1]
        while register_width > nextFieldStartingPos:
            if nextFieldStartingPos != bitOffsetList[index]:
                newBitWidth = bitOffsetList[index] - nextFieldStartingPos
                bitOffsetList.insert(index, nextFieldStartingPos)
                fieldNameList.insert(index, 'unused' + str(unUsedCnt))
                bitWidthList.insert(index, newBitWidth)
                fieldDescList.insert(index, 'unused')
                enumTypeList.insert(index, '')
                unUsedCnt += 1
            nextFieldStartingPos = int(bitOffsetList[index]) + int(bitWidthList[index])
            index += 1
        if (nextFieldStartingPos < size):
            bitOffsetList.insert(index, nextFieldStartingPos)
            fieldNameList.insert(index, 'unused' + str(unUsedCnt))
            bitWidthList.insert(index, size - nextFieldStartingPos)
            fieldDescList.insert(index, 'unused')
            enumTypeList.insert(index, '')

    return regName, fieldNameList, bitOffsetList, bitWidthList, fieldDescList, enumTypeList


class documentClass():
    def __init__(self, name):
        self.name = name
        self.memoryMapList = []

    def addMemoryMap(self, memoryMap):
        self.memoryMapList.append(memoryMap)


class memoryMapClass():
    def __init__(self, name):
        self.name = name
        self.addressBlockList = []

    def addAddressBlock(self, addressBlock):
        self.addressBlockList.append(addressBlock)


class addressBlockClass():
    def __init__(self, name, description, baseAddress, addrWidth, dataWidth):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = ""

    def addRegister(self, reg):
        assert isinstance(reg, registerClass)
        self.registerList.append(reg)

    def setRegisterList(self, registerList):
        self.registerList = registerList

    def returnAsString(self):
        raise NotImplementedError("method returnAsString() is virutal and must be overridden.")


class registerClass():
    def __init__(self, name, address, resetValue, size, access, desc, fieldNameList,
                 bitOffsetList, bitWidthList, fieldDescList, enumTypeList):
        assert isinstance(enumTypeList, list), 'enumTypeList is not a list'
        self.name = name
        self.address = address
        self.resetValue = resetValue
        self.size = size
        self.access = access
        self.desc = desc
        self.fieldNameList = fieldNameList
        self.bitOffsetList = bitOffsetList
        self.bitWidthList = bitWidthList
        self.fieldDescList = fieldDescList
        self.enumTypeList = enumTypeList


class enumTypeClassRegistry():
    """ should perhaps be a singleton instead """

    def __init__(self):
        self.listOfEnums = []

    def enumAllReadyExist(self, enum):
        for e in self.listOfEnums:
            if e.compare(enum):
                enum.allReadyExist = True
                enum.enumName = e.name
                break
        self.listOfEnums.append(enum)
        return enum


class enumTypeClass():
    def __init__(self, name, bitWidth, keyList, valueList, descrList):
        self.name = name
        self.bitWidth = bitWidth
        matrix = list(zip(valueList, keyList, descrList))
        matrix.sort(key=lambda x: x[0])
        valueList, keyList, descrList = list(zip(*matrix))
        self.keyList = list(keyList)
        self.valueList = list(valueList)
        self.allReadyExist = False
        self.enumName = None
        self.descrList = descrList

    def compare(self, other):
        result = True
        result = self.bitWidth == other.bitWidth and result
        result = self.compareLists(self.keyList, other.keyList) and result
        result = self.compareLists(self.valueList, other.valueList) and result

        return result

    def compareLists(self, list1, list2):
        return list1 == list2


class rstAddressBlock(addressBlockClass):
    """Generates a ReStructuredText file from a IP-XACT register description"""

    def __init__(self, name, description, baseAddress, addrWidth, dataWidth, config):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = ".rst"
        self.config = config

    def returnEnumValueString(self, enumTypeObj):
        if isinstance(enumTypeObj, enumTypeClass):
            l = []
            for i in range(len(enumTypeObj.keyList)):
                l.append(enumTypeObj.keyList[i] + '=' + enumTypeObj.valueList[i])
            s = ", ".join(l)
        else:
            s = ''
        return s

    def returnAsString(self):
        r = RstCloth(io.StringIO())  # with default parameter, sys.stdout is used
        regNameList = [reg.name for reg in self.registerList]
        regAddressList = [reg.address for reg in self.registerList]
        regDescrList = [reg.desc for reg in self.registerList]

        r.title(self.name)  # Use the name of the addressBlock as title
        r.newline()
        r.content(self.description)
        r.newline()
        r.field("Base Address", hex(self.baseAddress))
        r.newline()
        r.h2("Registers")

        summary_table = []
        for i in range(len(regNameList)):
            summary_table.append(["%#04x" % regAddressList[i], str(regNameList[i]) + "_", str(regDescrList[i])])
        r.table(header=['Address', 'Register Name', 'Description'],
                data=summary_table)

        for reg in self.registerList:
            r.h2(reg.name)
            r.newline()
            r.field("Name", reg.name)
            r.field("Address", hex(reg.address))
            if reg.resetValue:
                # display the resetvalue in hex notation in the full length of the register
                r.field("Reset Value",
                             "{value:#0{size:d}x}".format(value=int(reg.resetValue, 0), size=reg.size // 4 + 2))
            r.field("Access", reg.access)
            r.field("Description", reg.desc)

            reg_table = []
            for fieldIndex in reversed(list(range(len(reg.fieldNameList)))):
                if reg.bitWidthList[fieldIndex] == 1:  # only one bit -> no range needed
                    bits = f"{reg.bitOffsetList[fieldIndex]}"
                else:
                     bits = f"[{reg.bitOffsetList[fieldIndex] + reg.bitWidthList[fieldIndex] - 1}:{reg.bitOffsetList[fieldIndex]}]"
                _line = [bits,
                         reg.fieldNameList[fieldIndex]]

                if reg.resetValue:
                    temp = (int(reg.resetValue, 0) >> reg.bitOffsetList[fieldIndex])
                    mask = (2 ** reg.bitWidthList[fieldIndex]) - 1
                    temp &= mask
                    temp = "{value:#0{width}x}".format(value=temp,
                                                       width=math.ceil(reg.bitWidthList[fieldIndex] / 4) + 2)
                    _line.append(temp)
                _line.append(reg.fieldDescList[fieldIndex])
                reg_table.append(_line)

            _headers = ['Bits', 'Field name']
            if reg.resetValue:
                _headers.append('Reset')
            _headers.append('Description')
            r.table(header=_headers,
                    data=reg_table)

            # enumerations
            for enum in reg.enumTypeList:
                if enum:
                    # header
                    r.h3(enum.name)
                    # table
                    enum_table = []
                    for i in range(len(enum.keyList)):
                        _value = "{value:#0{width}x}".format(value=int(enum.valueList[i], 0),
                                                             width=math.ceil(int(enum.bitWidth, 0) / 4) + 2)

                        _line = [enum.keyList[i],
                                 _value,
                                 enum.descrList[i]]
                        enum_table.append(_line)
                    r.table(header=['Name', 'Value', 'Description'],
                            data=enum_table)

        return r.data


class mdAddressBlock(addressBlockClass):
    """Generates a Markdown file from a IP-XACT register description"""

    def __init__(self, name, description, baseAddress, addrWidth, dataWidth, config):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = ".md"
        self.mdFile = MdUtils(file_name="none",
                              title="")

    def returnEnumValueString(self, enumTypeObj):
        if isinstance(enumTypeObj, enumTypeClass):
            l = []
            for i in range(len(enumTypeObj.keyList)):
                l.append(enumTypeObj.keyList[i] + '=' + enumTypeObj.valueList[i])
            s = ", ".join(l)
        else:
            s = ''
        return s

    def returnAsString(self):
        regNameList = [reg.name for reg in self.registerList]
        regAddressList = [reg.address for reg in self.registerList]
        regDescrList = [reg.desc for reg in self.registerList]

        self.mdFile.new_header(level=1, title=self.name)  # Use the name of the addressBlock as title
        self.mdFile.new_paragraph(self.description)
        self.mdFile.new_paragraph(f"Base Address: {self.baseAddress:#x}")
        self.mdFile.new_paragraph()
        self.mdFile.new_header(level=2, title="Registers")

        # summary
        header = ['Address', 'Register Name', 'Description']
        rows = []
        for i in range(len(regNameList)):
            rows.extend(["{:#04x}".format(regAddressList[i]),
                         f"[{regNameList[i]}](#{regNameList[i]})",
                         str(regDescrList[i])])
        self.mdFile.new_table(columns=len(header),
                              rows=len(regNameList) + 1,  # header + data
                              text=header + rows,
                              text_align='left')

        # all registers
        for reg in self.registerList:
            headers = ['Bits', 'Field name']
            if reg.resetValue:
                headers.append('Reset')
            headers.append('Description')

            self.returnMdRegDesc(reg.name, reg.address, reg.size, reg.resetValue, reg.desc, reg.access)
            reg_table = []
            for fieldIndex in reversed(list(range(len(reg.fieldNameList)))):
                if reg.bitWidthList[fieldIndex] == 1:  # only one bit -> no range needed
                    bits = f"{reg.bitOffsetList[fieldIndex]}"
                else:
                     bits = f"[{reg.bitOffsetList[fieldIndex] + reg.bitWidthList[fieldIndex] - 1}:{reg.bitOffsetList[fieldIndex]}]"
                reg_table.append(bits)
                reg_table.append(reg.fieldNameList[fieldIndex])
                if reg.resetValue:
                    temp = (int(reg.resetValue, 0) >> reg.bitOffsetList[fieldIndex])
                    mask = (2 ** reg.bitWidthList[fieldIndex]) - 1
                    temp &= mask
                    temp = "{value:#0{width}x}".format(value=temp,
                                                       width=math.ceil(reg.bitWidthList[fieldIndex] / 4) + 2)
                    reg_table.append(temp)
                reg_table.append(reg.fieldDescList[fieldIndex])

            self.mdFile.new_table(columns=len(headers),
                                  rows=len(reg.fieldNameList) + 1,
                                  text=headers + reg_table,
                                  text_align='left')

            # enumerations
            for enum in reg.enumTypeList:
                if enum:
                    self.mdFile.new_header(level=4,
                                           title=enum.name)
                    enum_table = []
                    for i in range(len(enum.keyList)):
                        _value = "{value:#0{width}x}".format(value=int(enum.valueList[i], 0),
                                                             width=math.ceil(int(enum.bitWidth, 0) / 4) + 2)
                        enum_table.append(enum.keyList[i])
                        enum_table.append(_value)
                        enum_table.append(enum.descrList[i])
                    headers = ['Name', 'Value', 'Description']
                    self.mdFile.new_table(columns=len(headers),
                                          rows=len(enum.keyList) + 1,
                                          text=headers + enum_table,
                                          text_align='left')

        return self.mdFile.file_data_text

    def returnMdRegDesc(self, name, address, size, resetValue, desc, access):
        self.mdFile.new_header(level=3, title=name)
        self.mdFile.new_line("**Name** " + str(name))
        self.mdFile.new_line("**Address** " + hex(address))
        if resetValue:
            # display the resetvalue in hex notation in the full length of the register
            self.mdFile.new_line(
                "**Reset Value** {value:#0{size:d}x}".format(value=int(resetValue, 0), size=size // 4 + 2))
        self.mdFile.new_line("**Access** " + access)
        self.mdFile.new_line("**Description** " + desc)


class vhdlAddressBlock(addressBlockClass):
    """Generates a vhdl file from a IP-XACT register description"""

    def __init__(self, name, description, baseAddress, addrWidth, dataWidth, config):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = "_vhd_pkg.vhd"
        self.config = config
        if self.config['vhdl']['std'] == "resolved":
            self.std = "std_logic"
            self.sulv = "slv"  # Std_Logic_Vector
        else:
            self.std = "std_ulogic"
            self.sulv = "sulv"  # Std_ULogic_Vector

    def returnAsString(self):
        r = ''
        r += self.returnPkgHeaderString()
        r += "\n\n"
        r += self.returnPkgBodyString()
        return r

    def returnPkgHeaderString(self):
        r = ''
        r += "--\n"
        r += "-- Automatically generated\n"
        r += f"-- with the command '{' '.join(sys.argv)}'\n"
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
        r += f"  constant addr_width : natural := {self.addrWidth};\n"
        r += f"  constant data_width : natural := {self.dataWidth};\n"

        r += "\n\n"

        r += self.returnRegFieldEnumTypeStrings(True)

        for reg in self.registerList:
            _width = math.ceil(self.addrWidth / 4) + 2  # +2 for the '0x'
            r += f"  constant {reg.name}_addr : natural := {reg.address} ;  -- {reg.address:#0{_width}x}\n"
        r += "\n"

        for reg in self.registerList:
            if reg.resetValue:
                _value = int(reg.resetValue, 0)
                _width = math.ceil((self.dataWidth / 4)) + 2  # +2 for the '0x'
                r += f"  constant {reg.name}_reset_value : {self.std}_vector(data_width-1 downto 0) := {self.std}_vector(to_unsigned({_value:d}, data_width));  -- {_value:#0{_width}x}\n"

        r += "\n\n"

        for reg in self.registerList:
            r += self.returnRegRecordTypeString(reg)

        r += self.returnRegistersInRecordTypeString()
        r += self.returnRegistersOutRecordTypeString()
        r += self.returnRegistersReadFunction()
        r += self.returnRegistersWriteFunction()
        r += self.returnRegistersResetFunction()

        if self.config['vhdl'].getboolean('PublicConvFunct'):
            for reg in self.registerList:
                r += self.returnRecToSulvFunction(reg)
                r += self.returnSulvToRecFunction(reg)

        r += "end;\n"

        return r

    def returnRegFieldEnumTypeStrings(self, prototype):
        r = ''
        for reg in self.registerList:
            for enum in reg.enumTypeList:
                if isinstance(enum, enumTypeClass) and not enum.allReadyExist:
                    r += f"  -- {enum.name}\n"  # group the enums in the package
                    if prototype:
                        t = f"  type {enum.name}_enum is ("
                        indent = t.find('(') + 1
                        r += t
                        for ki in range(len(enum.keyList)):
                            if ki != 0:  # no indentation for the first element
                                r += " " * indent
                            r += enum.keyList[ki]
                            if ki != len(enum.keyList) - 1:  # no ',' for the last element
                                r += ","
                            else:  # last element
                                r += ");"
                            if enum.descrList[ki]:
                                r += f"  -- {enum.descrList[ki]}"
                            if ki != len(enum.keyList) - 1:  # no new line for the last element
                                r += "\n"
                        r += "\n"

                    r += f"  function {enum.name}_enum_to_{self.sulv}(v: {enum.name}_enum) return {self.std}_vector"
                    if prototype:
                        r += ";\n"
                    else:
                        r += " is\n"
                        r += f"    variable r : {self.std}_vector({enum.bitWidth}-1 downto 0);\n"
                        r += "  begin\n"
                        r += "       case v is\n"
                        for i in range(len(enum.keyList)):
                            r += '         when {key} => r:="{value_int:0{bitwidth}b}"; -- {value}\n'.format(
                                key=enum.keyList[i],
                                value=enum.valueList[i],
                                value_int=int(enum.valueList[i], 0),
                                bitwidth=int(enum.bitWidth, 0))
                        r += "       end case;\n"
                        r += "    return r;\n"
                        r += "  end function;\n\n"

                    r += f"  function {self.sulv}_to_{enum.name}_enum(v: {self.std}_vector({enum.bitWidth}-1 downto 0)) return {enum.name}_enum"
                    if prototype:
                        r += ";\n"
                    else:
                        r += " is\n"
                        r += f"    variable r : {enum.name}_enum;\n"
                        r += "  begin\n"
                        r += "       case v is\n"
                        for i in range(len(enum.keyList)):
                            r += '         when "{value_int:0{bitwidth}b}" => r:={key};\n'.format(key=enum.keyList[i],
                                                                                                  value_int=int(enum.valueList[i], 0),
                                                                                                  bitwidth=int(enum.bitWidth, 0))
                        r += f"         when others => r:={enum.keyList[0]}; -- error\n"
                        r += "       end case;\n"
                        r += "    return r;\n"
                        r += "  end function;\n\n"

                    if prototype:
                        r += "\n"
        if prototype:
            r += "\n"
        return r

    def returnRegRecordTypeString(self, reg):
        r = ''
        r += f"  type {reg.name}_record_type is record\n"
        for i in reversed(list(range(len(reg.fieldNameList)))):
            bits = f"[{reg.bitOffsetList[i] + reg.bitWidthList[i] - 1}:{reg.bitOffsetList[i]}]"
            bit = f"[{reg.bitOffsetList[i]}]"
            if isinstance(reg.enumTypeList[i], enumTypeClass):
                if not reg.enumTypeList[i].allReadyExist:
                    r += f"    {reg.fieldNameList[i]} : {reg.enumTypeList[i].name}_enum; -- {bits}\n"
                else:
                    r += f"    {reg.fieldNameList[i]} : {reg.enumTypeList[i].enumName}_enum; -- {bits}\n"
            else:
                if reg.bitWidthList[i] == 1:  # single bit
                    r += f"    {reg.fieldNameList[i]} : {self.std}; -- {bit}\n"
                else:  # vector
                    r += f"    {reg.fieldNameList[i]} : {self.std}_vector({reg.bitWidthList[i] - 1} downto 0); -- {bits}\n"
        r += "  end record;\n\n"
        return r

    def returnRegistersInRecordTypeString(self):
        r = ""
        r += f"  type {self.name}_in_record_type is record\n"
        for reg in self.registerList:
            if reg.access == "read-only":
                _width = math.ceil(self.addrWidth / 4) + 2  # +2 for the '0x'
                r += f"    {reg.name} : {reg.name}_record_type; -- addr {reg.address:#0{_width}x}\n"
        r += "  end record;\n\n"
        return r

    def returnRegistersOutRecordTypeString(self):
        r = ""
        r += f"  type {self.name}_out_record_type is record\n"
        for reg in self.registerList:
            if reg.access != "read-only":
                _width = math.ceil(self.addrWidth / 4) + 2  # +2 for the '0x'
                r += f"    {reg.name} : {reg.name}_record_type; -- addr {reg.address:#0{_width}x}\n"
        r += "  end record;\n\n"
        return r

    def returnRegistersReadFunction(self):
        r = f"  function read_{self.name}(registers_i : {self.name}_in_record_type;\n"
        indent = " " * (r.find('(') + 1)
        r += f"{indent}registers_o : {self.name}_out_record_type;\n"
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0)\n"
        r += f"{indent}) return {self.std}_vector;\n\n"
        return r

    def returnRegistersWriteFunction(self):
        r = f"  function write_{self.name}(value : {self.std}_vector(data_width-1 downto 0);\n"
        indent = " " * (r.find('(') + 1)
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0);\n"
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type;\n\n"
        return r

    def returnRegistersResetFunction(self):
        r = f"  function reset_{self.name} return {self.name}_out_record_type;\n"
        r += f"  function reset_{self.name}(address: {self.std}_vector(addr_width-1 downto 0);\n"
        indent = " " * (r.splitlines()[-1].find('(') + 1)
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type;\n\n"
        return r

    def returnRecToSulvFunctionString(self, reg):
        r = ""
        r += f"  function {reg.name}_record_type_to_{self.sulv}(v : {reg.name}_record_type) return {self.std}_vector is\n"
        r += f"    variable r : {self.std}_vector(data_width-1 downto 0);\n"
        r += "  begin\n"
        r += "    r :=  (others => '0');\n"
        for i in reversed(list(range(len(reg.fieldNameList)))):
            bits = f"{reg.bitOffsetList[i] + reg.bitWidthList[i] - 1} downto {reg.bitOffsetList[i]}"
            bit = str(reg.bitOffsetList[i])
            if isinstance(reg.enumTypeList[i], enumTypeClass):
                if not reg.enumTypeList[i].allReadyExist:
                    r += f"    r({bits}) := {reg.enumTypeList[i].name}_enum_to_{self.sulv}(v.{reg.fieldNameList[i]});\n"
                else:
                    r += f"    r({bits}) := {reg.enumTypeList[i].enumName}_enum_to_{self.sulv}(v.{reg.fieldNameList[i]});\n"
            else:
                if reg.bitWidthList[i] == 1:  # single bit
                    r += f"    r({bit}) := v.{reg.fieldNameList[i]};\n"
                else:  # vector
                    r += f"    r({bits}) := v.{reg.fieldNameList[i]};\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def returnRecToSulvFunction(self, reg):
        r = f"  function {reg.name}_record_type_to_{self.sulv}(v : {reg.name}_record_type) return {self.std}_vector;\n\n"
        return r

    def returnSulvToRecFunctionString(self, reg):
        r = ""
        r += f"  function {self.sulv}_to_{reg.name}_record_type(v : {self.std}_vector) return {reg.name}_record_type is\n"
        r += f"    variable r : {reg.name}_record_type;\n"
        r += "  begin\n"
        for i in reversed(list(range(len(reg.fieldNameList)))):
            bits = f"{reg.bitOffsetList[i] + reg.bitWidthList[i] - 1} downto {reg.bitOffsetList[i]}"
            bit = str(reg.bitOffsetList[i])
            if isinstance(reg.enumTypeList[i], enumTypeClass):
                if not reg.enumTypeList[i].allReadyExist:
                    r += f"    r.{reg.fieldNameList[i]} := {self.sulv}_to_{reg.enumTypeList[i].name}_enum(v({bits}));\n"
                else:
                    r += f"    r.{reg.fieldNameList[i]} := {self.sulv}_to_{reg.enumTypeList[i].enumName}_enum(v({bits}));\n"
            else:
                if reg.bitWidthList[i] == 1:  # single bit
                    r += f"    r.{reg.fieldNameList[i]} := v({bit});\n"
                else:
                    r += f"    r.{reg.fieldNameList[i]} := v({bits});\n"
        r += "    return r;\n"
        r += "  end function;\n\n"

        return r

    def returnSulvToRecFunction(self, reg):
        r = f"  function {self.sulv}_to_{reg.name}_record_type(v : {self.std}_vector) return {reg.name}_record_type;\n\n"
        return r

    def returnReadFunctionString(self):
        r = ""
        t = f"  function read_{self.name}(registers_i : {self.name}_in_record_type;\n"
        indent = " " * (t.find('(') + 1)
        r += t
        r += f"{indent}registers_o : {self.name}_out_record_type;\n"
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0)\n"
        r += f"{indent}) return {self.std}_vector is\n"
        r += f"    variable r : {self.std}_vector(data_width-1 downto 0);\n"
        r += "  begin\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.registerList:
            if reg.access == "read-only":
                r += f"      when {reg.name}_addr => r:= {reg.name}_record_type_to_{self.sulv}(registers_i.{reg.name});\n"
            else:
                r += f"      when {reg.name}_addr => r:= {reg.name}_record_type_to_{self.sulv}(registers_o.{reg.name});\n"
        r += "      when others => r := (others => '0');\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def returnWriteFunctionString(self):
        r = ""
        t = f"  function write_{self.name}(value : {self.std}_vector(data_width-1 downto 0);\n"
        r += t
        indent = " " * (t.find('(') + 1)
        r += f"{indent}address : {self.std}_vector(addr_width-1 downto 0);\n"
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        r += "    r := registers_o;\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.registerList:
            if reg.access != "read-only":
                r += f"         when {reg.name}_addr => r.{reg.name} := {self.sulv}_to_{reg.name}_record_type(value);\n"
        r += "      when others => null;\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def returnResetFunctionString(self):
        r = ""
        r += f"  function reset_{self.name} return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        for reg in self.registerList:
            if reg.resetValue:
                if reg.access != "read-only":
                    r += f"         r.{reg.name} := {self.sulv}_to_{reg.name}_record_type({reg.name}_reset_value);\n"
        r += "    return r;\n"
        r += "  end function;\n"
        r += "\n"
        r += f"  function reset_{self.name}(address: {self.std}_vector(addr_width-1 downto 0);\n"
        indent = " " * (r.splitlines()[-1].find('(') + 1)
        r += f"{indent}registers_o : {self.name}_out_record_type\n"
        r += f"{indent}) return {self.name}_out_record_type is\n"
        r += f"    variable r : {self.name}_out_record_type;\n"
        r += "  begin\n"
        r += "    r := registers_o;\n"
        r += "    case to_integer(unsigned(address)) is\n"
        for reg in self.registerList:
            if reg.resetValue:
                if reg.access != "read-only":
                    r += f"         when {reg.name}_addr => r.{reg.name} := {self.sulv}_to_{reg.name}_record_type({reg.name}_reset_value);\n"
        r += "      when others => null;\n"
        r += "    end case;\n"
        r += "    return r;\n"
        r += "  end function;\n\n"
        return r

    def returnPkgBodyString(self):
        r = ""
        r += f"package body {self.name}_vhd_pkg is\n\n"

        r += self.returnRegFieldEnumTypeStrings(False)

        for reg in self.registerList:
            r += self.returnRecToSulvFunctionString(reg)
            r += self.returnSulvToRecFunctionString(reg)

        r += self.returnReadFunctionString()
        r += self.returnWriteFunctionString()
        r += self.returnResetFunctionString()
        r += "end package body;\n"
        return r


class systemVerilogAddressBlock(addressBlockClass):
    def __init__(self, name, description, baseAddress, addrWidth, dataWidth, config):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = "_sv_pkg.sv"
        self.config = config

    def returnIncludeString(self):
        r = "\n"
        r += "`define " + self.name + "_addr_width " + str(self.addrWidth) + "\n"
        r += "`define " + self.name + "_data_width " + str(self.dataWidth) + "\n"
        return r

    def returnSizeString(self):
        r = "\n"
        r += "const int addr_width = " + str(self.addrWidth) + ";\n"
        r += "const int data_width = " + str(self.dataWidth) + ";\n"
        return r

    def returnAddressesString(self):
        r = "\n"
        for reg in self.registerList:
            r += "const int " + reg.name + "_addr = " + str(reg.address) + ";\n"
        r += "\n"
        return r

    def returnAddressListString(self):
        r = "\n"
        r = "//synopsys translate_off\n"
        r += "const int " + self.name + "_regAddresses [" + str(len(self.registerList)) + "] = '{"
        l = []
        for reg in self.registerList:
            l.append("\n     " + reg.name + "_addr")

        r += ",".join(l)
        r += "};\n"
        r += "\n"
        r += "const string " + self.name + "_regNames [" + str(len(self.registerList)) + "] = '{"
        l = []
        for reg in self.registerList:
            l.append('\n      "' + reg.name + '"')
        r += ",".join(l)
        r += "};\n"

        r += "const reg " + self.name + "_regUnResetedAddresses [" + str(len(self.registerList)) + "] = '{"
        l = []
        for reg in self.registerList:
            if reg.resetValue:
                l.append("\n   1'b0")
            else:
                l.append("\n   1'b1")
        r += ",".join(l)
        r += "};\n"
        r += "\n"
        r += "//synopsys translate_on\n\n"
        return r

    def enumeratedType(self, prepend, fieldName, valueNames, values):
        r = "\n"
        members = []
        # dont want to create to simple names in the global names space.
        # should preppend with name from ipxact file
        for index in range(len(valueNames)):
            name = valueNames[index]
            value = values[index]
            members.append(name + "=" + value)
        r += "typedef enum { " + ",".join(members) + "} enum_" + fieldName + ";\n"
        return r

    def returnResetValuesString(self):
        r = ""
        for reg in self.registerList:
            if reg.resetValue:
                r += "const " + reg.name + "_struct_type " + reg.name + \
                     "_reset_value = " + str(int(reg.resetValue, 0)) + ";\n"
        r += "\n"
        return r

    def returnStructString(self):
        r = "\n"
        for reg in self.registerList:
            r += "\ntypedef struct packed {\n"
            for i in reversed(list(range(len(reg.fieldNameList)))):
                bits = "bits [" + str(reg.bitOffsetList[i] + reg.bitWidthList[i] - 1) + \
                       ":" + str(reg.bitOffsetList[i]) + "]"
                r += "   bit [" + str(reg.bitWidthList[i] - 1) + ":0] " + \
                     str(reg.fieldNameList[i]) + ";//" + bits + "\n"
            r += "} " + reg.name + "_struct_type;\n\n"
        return r

    def returnRegistersStructString(self):
        r = "typedef struct packed {\n"
        for reg in self.registerList:
            r += "   " + reg.name + "_struct_type " + reg.name + ";\n"
        r += "} " + self.name + "_struct_type;\n\n"
        return r

    def returnReadFunctionString(self):
        r = "function bit [31:0] read_" + self.name + "(" + self.name + "_struct_type registers,int address);\n"
        r += "      bit [31:0]  r;\n"
        r += "      case(address)\n"
        for reg in self.registerList:
            r += "         " + reg.name + "_addr: r[$bits(registers." + reg.name + ")-1:0] = registers." + reg.name + ";\n"
        r += "        default: r =0;\n"
        r += "      endcase\n"
        r += "      return r;\n"
        r += "endfunction\n\n"
        return r

    def returnWriteFunctionString(self):
        t = "function " + self.name + "_struct_type write_" + self.name + "(bit [31:0] data, int address,\n"
        r = t
        indent = r.find('(') + 1
        r += " " * indent + self.name + "_struct_type registers);\n"
        r += "   " + self.name + "_struct_type r;\n"
        r += "   r = registers;\n"
        r += "   case(address)\n"
        for reg in self.registerList:
            r += "         " + reg.name + "_addr: r." + reg.name + " = data[$bits(registers." + reg.name + ")-1:0];\n"
        r += "   endcase // case address\n"
        r += "   return r;\n"
        r += "endfunction\n\n"
        return r

    def returnResetFunctionString(self):
        r = "function " + self.name + "_struct_type reset_" + self.name + "();\n"
        r += "   " + self.name + "_struct_type r;\n"
        for reg in self.registerList:
            if reg.resetValue:
                r += "   r." + reg.name + "=" + reg.name + "_reset_value;\n"
        r += "   return r;\n"
        r += "endfunction\n"
        r += "\n"
        return r

    def returnAsString(self):
        r = ''
        r += "// Automatically generated\n"
        r += "// with the command '%s'\n" % (' '.join(sys.argv))
        r += "//\n"
        r += "// Do not manually edit!\n"
        r += "//\n"
        r += "package " + self.name + "_sv_pkg;\n\n"
        r += self.returnSizeString()
        r += self.returnAddressesString()
        r += self.returnAddressListString()
        r += self.returnStructString()
        r += self.returnResetValuesString()
        r += self.returnRegistersStructString()
        r += self.returnReadFunctionString()
        r += self.returnWriteFunctionString()
        r += self.returnResetFunctionString()
        r += "endpackage //" + self.name + "_sv_pkg\n"
        return r


class cAddressBlock(addressBlockClass):
    def __init__(self, name, description, baseAddress, addrWidth, dataWidth, config):
        self.name = name
        self.description = description
        self.baseAddress = baseAddress
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList = []
        self.suffix = ".h"

    def registerOffsetName(self, reg):
        return self.name.upper() +"_" + reg.name.upper() + "_OFFSET"

    def registerResetName(self, reg):
        return self.name.upper() +"_" + reg.name.upper() + "_RESET"

    def getFieldMaskName(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_MASK"

    def getFieldShiftName(self, reg, fieldname):
        return self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper() + "_SHIFT"

    def getMacroName(self, reg, fieldname):
        return "GET_" + self.name.upper() + "_" + reg.name.upper() + "_" + fieldname.upper()

    def returnRegisterOffsets(self):
        r = ""
        r += "// ------------------------------------------------\n"
        r += "//  Register offsets\n"
        r += "// ------------------------------------------------\n"
        for reg in self.registerList:
            addrStr = "0x%0.2X" % reg.address
            r += "#define "+ self.registerOffsetName(reg) + "\t" + addrStr + "\t// " + reg.desc +"\n"

        r += "\n\n"
        return r

    def returnRegisterBitOperators(self):
        r = ""

        for reg in self.registerList:
            r += "// ------------------------------------------------\n"
            r += "//  Bit operations for register " + reg.name + "\n"
            r += "// ------------------------------------------------\n"
            for i in list(range(len(reg.fieldNameList))):
                fieldname = reg.fieldNameList[i]
                r += "#define "+ self.getFieldShiftName(reg, fieldname) + "\t" + \
                     str(reg.bitOffsetList[i]) + "\n"
                mask = 2 ** reg.bitWidthList[i] -1;
                maskStr = "0x%0.2X" % mask
                r += "#define "+ self.getFieldMaskName(reg, fieldname)  + " \t" + \
                     maskStr + "\n"

                r += "\n"

        return r

    def returnMacrosFunctions(self):
        r = ""

        for reg in self.registerList:
            r += "\n"
            r += "// ------------------------------------------------\n"
            r += "//  Macro functions for register " + reg.name + "\n"
            for i in list(range(len(reg.fieldNameList))):
                fieldname = reg.fieldNameList[i]
                l = f"//  - {self.getMacroName(reg, fieldname)} : {reg.fieldDescList[i]}"
                l = l.strip()  # avoid a space at the end of the line if field description is empty
                r += l + "\n"
            r += "// ------------------------------------------------\n"
            r += "\n"
            for fieldname in reg.fieldNameList:
                operation = "((a >> " + self.getFieldShiftName(reg, fieldname) + \
                            ") & " + self.getFieldMaskName(reg, fieldname) + ")"

                r += "#define "+ self.getMacroName(reg, fieldname) + "(a)\t" + operation + "\n"

        return r

    def returnAsString(self):
        r = ''
        r += "#pragma once\n"
        r += "/* Automatically generated\n"
        r += " * with the command '%s'\n" % (' '.join(sys.argv))
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

        r += self.returnRegisterOffsets()
        r += self.returnRegisterBitOperators()
        r += self.returnMacrosFunctions()

        r += "\n"
        r += "// End of " + self.name + self.suffix + "\n"
        return r


class ipxactParser():
    def __init__(self, srcFile, config):
        self.srcFile = srcFile
        self.config = config
        self.enumTypeClassRegistry = enumTypeClassRegistry()

    def returnDocument(self):
        spirit_ns = 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5'
        tree = ETree.parse(self.srcFile)
        ETree.register_namespace('spirit', spirit_ns)
        namespace = tree.getroot().tag[1:].split("}")[0]
        spiritString = '{' + spirit_ns + '}'
        docName = tree.find(spiritString + "name").text
        d = documentClass(docName)
        memoryMaps = tree.find(spiritString + "memoryMaps")
        memoryMapList = memoryMaps.findall(spiritString + "memoryMap") if memoryMaps is not None else []
        for memoryMap in memoryMapList:
            memoryMapName = memoryMap.find(spiritString + "name").text
            addressBlockList = memoryMap.findall(spiritString + "addressBlock")
            m = memoryMapClass(memoryMapName)
            for addressBlock in addressBlockList:
                # check first whether there is a description field
                if addressBlock.find(spiritString + "description") != None:
                    description = addressBlock.find(spiritString + "description").text
                else:
                    description = ""
                addressBlockName = addressBlock.find(spiritString + "name").text
                registerList = addressBlock.findall(spiritString + "register")
                baseAddress = int(addressBlock.find(spiritString + "baseAddress").text, 0)
                nbrOfAddresses = int(addressBlock.find(spiritString + "range").text, 0)  # TODO, this is wrong
                addrWidth = int(math.ceil((math.log(baseAddress + nbrOfAddresses, 2))))
                dataWidth = int(addressBlock.find(spiritString + "width").text, 0)
                a = addressBlockClass(addressBlockName,
                                      description,
                                      baseAddress,
                                      addrWidth,
                                      dataWidth)
                for registerElem in registerList:
                    regName = registerElem.find(spiritString + "name").text
                    reset = registerElem.find(spiritString + "reset")
                    if reset is not None:
                        resetValue = reset.find(spiritString + "value").text
                    else:
                        resetValue = None
                    size = int(registerElem.find(spiritString + "size").text, 0)
                    access = registerElem.find(spiritString + "access").text
                    if registerElem.find(spiritString + "description") != None:
                        desc = registerElem.find(spiritString + "description").text
                    else:
                        desc = ""
                    regAddress = baseAddress + int(registerElem.find(spiritString + "addressOffset").text, 0)
                    r = self.returnRegister(spiritString, registerElem, regAddress,
                                            resetValue, size, access, desc, dataWidth)
                    a.addRegister(r)
                m.addAddressBlock(a)
            d.addMemoryMap(m)

        return d

    def returnRegister(self, spiritString, registerElem, regAddress, resetValue, size, access, regDesc, dataWidth):
        regName = registerElem.find(spiritString + "name").text
        fieldList = registerElem.findall(spiritString + "field")
        fieldNameList = [item.find(spiritString + "name").text for item in fieldList]
        bitOffsetList = [item.find(spiritString + "bitOffset").text for item in fieldList]
        bitWidthList = [item.find(spiritString + "bitWidth").text for item in fieldList]
        fieldDescList = []
        for item in fieldList:
            description = item.find(spiritString + "description")
            # handle no or an empty description
            if description is None:
                fieldDescList.append("")
            elif hasattr(description, 'text'):
                if description.text:
                    fieldDescList.append(description.text)
                else:
                    fieldDescList.append("")
            else:
                fieldDescList.append("")
        enumTypeList = []
        for index in range(len(fieldList)):
            fieldElem = fieldList[index]
            bitWidth = bitWidthList[index]
            fieldName = fieldNameList[index]
            enumeratedValuesElem = fieldElem.find(spiritString + "enumeratedValues")
            if enumeratedValuesElem is not None:
                enumeratedValueList = enumeratedValuesElem.findall(spiritString + "enumeratedValue")
                valuesNameList = [item.find(spiritString + "name").text for item in enumeratedValueList]
                descrList = [item.find(spiritString + "description").text if item.find(
                    spiritString + "description") is not None else "" for item in enumeratedValueList]
                valuesList = [item.find(spiritString + "value").text for item in enumeratedValueList]
                if len(valuesNameList) > 0:
                    if int(bitWidth) > 1:  # if the field of a enum is longer than 1 bit, always use enums
                        enum = enumTypeClass(fieldName, bitWidth, valuesNameList, valuesList, descrList)
                        enum = self.enumTypeClassRegistry.enumAllReadyExist(enum)
                        enumTypeList.append(enum)
                    else:  # bit field of 1 bit
                        if self.config['global'].getboolean('onebitenum'):  # do create one bit enums
                            enum = enumTypeClass(fieldName, bitWidth, valuesNameList, valuesList, descrList)
                            enum = self.enumTypeClassRegistry.enumAllReadyExist(enum)
                            enumTypeList.append(enum)
                        else:  # dont create enums of booleans because this only decreases readability
                            enumTypeList.append(None)
                else:
                    enumTypeList.append(None)
            else:
                enumTypeList.append(None)

        if len(fieldNameList) == 0:
            fieldNameList.append(regName)
            bitOffsetList.append(0)
            bitWidthList.append(dataWidth)
            fieldDescList.append('')
            enumTypeList.append(None)

        (regName, fieldNameList, bitOffsetList, bitWidthList, fieldDescList, enumTypeList) = sortRegisterAndFillHoles(
            regName, fieldNameList, bitOffsetList, bitWidthList, fieldDescList, enumTypeList, size,
            self.config['global'].getboolean('unusedholes'))

        reg = registerClass(regName, regAddress, resetValue, size, access, regDesc, fieldNameList,
                            bitOffsetList, bitWidthList, fieldDescList, enumTypeList)
        return reg


class ipxact2otherGenerator():
    def __init__(self, destDir, config, namingScheme="addressBlockName", ):
        self.destDir = destDir
        self.namingScheme = namingScheme
        self.config = config

    def write(self, fileName, string):
        _dest = os.path.join(self.destDir, fileName)
        print("writing file " + _dest)

        if not os.path.exists(os.path.dirname(_dest)):
            os.makedirs(os.path.dirname(_dest))

        with open(_dest, "w") as f:
            f.write(string)

    def generate(self, generatorClass, document):
        self.document = document
        docName = document.name
        for memoryMap in document.memoryMapList:
            mapName = memoryMap.name
            for addressBlock in memoryMap.addressBlockList:
                blockName = addressBlock.name

                block = generatorClass(addressBlock.name,
                                       addressBlock.description,
                                       addressBlock.baseAddress,
                                       addressBlock.addrWidth,
                                       addressBlock.dataWidth,
                                       self.config,
                                       )

                block.setRegisterList(addressBlock.registerList)
                s = block.returnAsString()
                if self.namingScheme == "addressBlockName":
                    fileName = blockName + block.suffix
                else:
                    fileName = docName + '_' + mapName + '_' + blockName + block.suffix

                self.write(fileName, s)

                if generatorClass == systemVerilogAddressBlock:
                    includeFileName = fileName + "h"
                    includeString = block.returnIncludeString()
                    self.write(includeFileName, includeString)
