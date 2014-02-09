#!/usr/bin/env python

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


from optparse import OptionParser
import glob
import os
import xml.etree.ElementTree as etree
import textwrap
import math

def to_bin_string(val,nbrOfBits):
    return format(val, 'b').zfill(nbrOfBits)


def sortRegisterAndFillHoles(regName,fieldNameList,bitOffsetList,
                             bitWidthList,fieldDescList,enumTypeList):
    #sort the lists, highest offset first
    fieldNameList = fieldNameList
    bitOffsetList= [int(x) for x in bitOffsetList]
    bitWidthList = [int(x) for x in bitWidthList]
    fieldDescList = fieldDescList
    enumTypeList = enumTypeList
    matrix = zip(bitOffsetList,fieldNameList,bitWidthList,fieldDescList,enumTypeList)
    matrix.sort(key=lambda x: x[0])#, reverse=True)
    bitOffsetList,fieldNameList,bitWidthList,fieldDescList,enumTypeList=zip(*matrix)
    # zip return tuples not lists
    fieldNameList = list(fieldNameList)
    bitOffsetList= list([int(x) for x in bitOffsetList])
    bitWidthList = list([int(x) for x in bitWidthList])
    fieldDescList = list(fieldDescList)
    enumTypeList = list(enumTypeList)
    unUsedCnt=0
    nextFieldStartingPos=0
    #fill up the holes
    index = 0
    while index < len(fieldNameList):
        if nextFieldStartingPos == bitOffsetList[index]:
            nextFieldStartingPos = int(bitOffsetList[index]) + int(bitWidthList[index])
        else:
            newBitWidth = bitOffsetList[index]-nextFieldStartingPos
            bitOffsetList.insert(index, nextFieldStartingPos)
            fieldNameList.insert(index, 'unused'+str(unUsedCnt))
            bitWidthList.insert(index,newBitWidth)
            fieldDescList.insert(index, 'unused')
            enumTypeList.insert(index, '')
            unUsedCnt+=1
            index = index + 1
        index = index + 1


    return regName,fieldNameList,bitOffsetList,bitWidthList,fieldDescList,enumTypeList



class rstTable:
    def __init__(self,widthList):
        self.widthList = widthList
        self.rowList =[]

    def addRow(self,row):
        self.rowList.append(self.splitRowInLines(row))

    def splitRowInLines(self,row):
        new_row = []
        for columnIndex in range(len(row)):
            element = row[columnIndex]
            s=str(element) 
            l = textwrap.wrap(s,self.widthList[columnIndex])
            for i in range(len(l)):
                #pad with whitespace
                s = l[i].ljust(self.widthList[columnIndex])
                l[i]= s
            new_row.append(l)            
        return new_row


    def linesInRowLeft(self,row):
        linesLeft=False        
        for c in row:
            if len(c)>0:
                linesLeft=True
        return linesLeft

    def returnRstRow(self,rowNbr):
        r=""
        row = self.rowList[rowNbr]
        while self.linesInRowLeft(row):
            for i in range(len(row)):
                    r=r + "|"      
                    if len(row[i])>0:
                        r = r + row[i][0]
                        row[i] = row[i][1:]
                    else:
                        r=r + self.widthList[i]*' '
            r=r + "+\n"
        for i in range(len(self.widthList)):
            r=r + "+"
            if rowNbr == 0:
                r=r + self.widthList[i]*'='
            else:
                r=r + self.widthList[i]*'-'
        r=r + "+\n"
        return r


    def returnRst(self):     
        r=""
        for i in range(len(self.widthList)):
            r=r + "+"
            r=r + self.widthList[i]*'-'
        r=r + "+\n"
        for rowNbr in range(len(self.rowList)):
            r=r +  self.returnRstRow(rowNbr)
        r=r + "\n"
        return r

class documentClass:
    def __init__(self,name):
        self.name = name
        self.memoryMapList = []

    def addMemoryMap(self,memoryMap):
        self.memoryMapList.append(memoryMap)

class memoryMapClass:
    def __init__(self,name):
        self.name = name
        self.addressBlockList=[]

    def addAddressBlock(self,addressBlock):
        self.addressBlockList.append(addressBlock)

class addressBlockClass:
    def __init__(self, name, addrWidth, dataWidth):
        self.name = name
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList=[]
        self.suffix = ""

    def addRegister(self,reg):
        self.registerList.append(reg)

    def setRegisterList(self,registerList):
        self.registerList = registerList

    def returnAsString(self):
        raise NotImplementedError("method returnAsString() is virutal and must be overridden.")


class registerClass:
    def __init__(self,name,address,resetValue,desc,fieldNameList,
                 bitOffsetList,bitWidthList,fieldDescList,enumTypeList):
        self.name=name
        self.address=address
        self.resetValue=resetValue
        self.desc=desc
        self.fieldNameList=fieldNameList
        self.bitOffsetList = bitOffsetList
        self.bitWidthList=bitWidthList
        self.fieldDescList=fieldDescList
        self.enumTypeList=enumTypeList



class enumTypeClassRegistry:
    """ should perhaps be a singleton instead """
    def __init__(self):
        self.listOfEnums = []

    def allReadyExist(self,enum):
        for e in self.listOfEnums:
            if e.compare(enum):
                enum.allReadyExist = True
                enum.enumName = e.name
                break
        self.listOfEnums.append(enum)
        return enum
    


class enumTypeClass:
    def __init__(self,name,bitWidth,keyList,valueList):        
        self.name=name
        self.bitWidth=bitWidth
        matrix = zip(valueList,keyList)
        matrix.sort(key=lambda x: x[0])
        valueList,keyList = zip(*matrix)
        self.keyList=list(keyList)
        self.valueList=list(valueList)
        self.allReadyExist = False
        self.enumName = None

    def compare(self,other):
        result = True
        result = self.bitWidth == other.bitWidth and result
        result = self.compareLists(self.keyList,other.keyList) and result
        return result
        
    def compareLists(self,list1, list2):
        for val in list1:
            if val in list2:
                return True
        return False
        





class rstAddressBlock(addressBlockClass):
    """Generates a ReStructuredText file from a IP-XACT register descripstion"""
        
    def __init__(self, name, addrWidth, dataWidth):
        self.name = name
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList=[]
        self.suffix = ".rst"

    def returnEnumValueString(self,enumTypeObj):
        if enumTypeObj is not None:
            l = []
            for i in range(len(enumTypeObj.keyList)):
                l.append(enumTypeObj.keyList[i] +'=' + enumTypeObj.valueList[i])
            s = ", ".join(l)
        else:
            s =''
        return s

    def returnAsString(self):
        r=""
        regNameList = [reg.name for reg in self.registerList]
        regAddressList = [reg.address for reg in self.registerList]
        
        r = r + self.returnRstTitle()
        r = r + self.returnRstSubTitle()

        widthList = [12,15]
        summaryTable = rstTable(widthList)
        summaryTable.addRow(['Address','Register Name'])
        for i in range(len(regNameList)):
            summaryTable.addRow([hex(regAddressList[i]),str(regNameList[i])+"_"])

        r=r + summaryTable.returnRst()
        
        for reg in self.registerList:
            r=r + self.returnRstRegDesc(reg.name,reg.address,reg.resetValue,reg.desc)            
            widthList = [12,15,10,20]
            regTable = rstTable(widthList)
            regTable.addRow(['Bits','Field name','Type','Description'])
            for fieldIndex in reversed(range(len(reg.fieldNameList))):
                bits = "["+str(reg.bitOffsetList[fieldIndex]+reg.bitWidthList[fieldIndex]-1)+":"+str(reg.bitOffsetList[fieldIndex])+"]"
                regTable.addRow([bits,
                                 reg.fieldNameList[fieldIndex],
                                 self.returnEnumValueString(reg.enumTypeList[fieldIndex]),
                                 reg.fieldDescList[fieldIndex]])
            r=r + regTable.returnRst()

        return r


    def returnRstTitle(self):
        r=''
        r=r + "====================\n"
        r=r + "Register description\n"
        r=r + "====================\n\n"
        return r

    def returnRstSubTitle(self):
        r=''
        r=r + "Registers\n"
        r=r + "---------\n\n"
        return r

    def returnRstRegDesc(self,name,address,resetValue,desc):
        r=""
        r=r + name + "\n"
        r=r + len(name)*'-' + "\n"
        r=r + "\n"
        r=r + ":Name:        " + str(name) + "\n"
        r=r + "\n"
        r=r + ":Address:     " + hex(address) + "\n"
        r=r + "\n"
        if resetValue:
            r=r + ":Reset Value: " + hex(int(resetValue)) + "\n"
            r=r + "\n"
        r=r + ":Description: " + desc + "\n"
        r=r + "\n"
        return r


class vhdlAddressBlock(addressBlockClass):
    """Generates a vhdl file from a IP-XACT register descripstion"""

    def __init__(self, name, addrWidth, dataWidth):
        self.name = name
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList=[]
        self.suffix = "_vhd_pkg.vhd"


    def returnAsString(self):
        r=''
        r=r + self.returnPkgHeaderString()
        r=r + self.returnPkgBodyString()
        return r

    def returnPkgHeaderString(self):
        r=''
        r=r + "-- VHDL 93\n"
        r=r + "library ieee;\n"
        r=r + "use ieee.std_logic_1164.all;\n"
        r=r + "use ieee.numeric_std.all;\n"
        r=r + "package "+self.name+"_vhd_pkg is\n"
        r=r + "  constant addr_width : natural := "+str(self.addrWidth)+";\n"
        r=r + "  constant data_width : natural := "+str(self.dataWidth)+";\n"
        
        r=r + "\n\n"
       
        r=r + self.returnRegFieldEnumTypeStrings(True)

        for reg in self.registerList:
            r=r + " constant " + reg.name + "_addr : natural := "+str(reg.address)+";\n"

        for reg in self.registerList:
            if reg.resetValue:
                r=r + " constant " + reg.name + "_reset_value : std_ulogic_vector (data_width-1 downto 0)"
                r=r + " := std_ulogic_vector( to_unsigned("+str(int(reg.resetValue))+", data_width ));\n"

        r=r + "\n\n"

        for reg in self.registerList:
            r = r + self.returnRegRecordTypeString(reg)
        
        r = r + self.returnRegistersRecordTypeString()


        r=r + "  function read_" + self.name + "(registers : " + self.name + "_record_type;\n"
        r=r + "                        address   : std_ulogic_vector (addr_width-1 downto 0)\n"
        r=r + "                        ) return std_ulogic_vector;\n\n"

        r=r + "  function write_" + self.name + "(value     : std_ulogic_vector (data_width-1 downto 0);\n"
        r=r + "                         address   : std_ulogic_vector (addr_width-1 downto 0);\n"
        r=r + "                         registers : " + self.name + "_record_type\n"
        r=r + "                         ) return " + self.name + "_record_type;\n\n"

        r=r + "  function reset_" + self.name + " return " + self.name + "_record_type;\n\n"



        r=r + "end;\n"

        return r

    def returnRegFieldEnumTypeStrings(self,prototype):
        r=''
        for reg in self.registerList:
            for enum in reg.enumTypeList: 
                if enum is not None and enum.allReadyExist==False:
                    if prototype:
                        s=",".join(enum.keyList)
                        r=r + "  type "+enum.name+"_enum is ("+s+");\n\n"


                    r=r + "  function "+enum.name+"_enum_to_sulv(v: " + enum.name + "_enum ) return std_ulogic_vector"
                    if prototype:
                        r=r + ";\n\n"
                    else:
                        r=r + " is\n"
                        r=r + "    variable r : std_ulogic_vector ("+str(enum.bitWidth)+"-1 downto 0);\n"
                        r=r + "  begin\n"
                        r=r + "       case v is\n"
                        for i in range(len(enum.keyList)):
                            r=r + '         when ' + enum.keyList[i]+' => r:="'+to_bin_string(int(enum.valueList[i]),int(enum.bitWidth))+'"; -- '+enum.valueList[i] +'\n'
                        r=r + "       end case;\n"
                        r=r + "    return r;\n"
                        r=r + "  end function;\n\n"                                

                    r=r + "  function sulv_to_"+enum.name+"_enum(v: std_ulogic_vector ("+str(enum.bitWidth)+"-1 downto 0)) return " + enum.name + "_enum"
                    if prototype:
                        r=r + ";\n\n"
                    else:
                        r=r + " is\n"
                        r=r + "    variable r : "+enum.name+"_enum;\n"
                        r=r + "  begin\n"
                        r=r + "       case v is\n"
                        for i in range(len(enum.keyList)):
                            r=r + '         when "'+to_bin_string(int(enum.valueList[i]),int(enum.bitWidth))+'" => r:=' + enum.keyList[i]+';\n'
                        r=r + '         when others => r:='+enum.keyList[0]+'; -- error \n'
                        r=r + "       end case;\n"
                        r=r + "    return r;\n"
                        r=r + "  end function;\n\n"                                






        return r



    def returnRegRecordTypeString(self,reg):
        r=''
        r=r + "  type "+reg.name+"_record_type is record\n"
        for i in reversed(range(len(reg.fieldNameList))):
            bits = "["+str(reg.bitOffsetList[i]+reg.bitWidthList[i]-1)+":"+str(reg.bitOffsetList[i])+"]"
            if reg.enumTypeList[i] is not None:
                if reg.enumTypeList[i].allReadyExist==False:
                    r=r + "    "+reg.fieldNameList[i]+" : "+reg.enumTypeList[i].name+"_enum; -- "+bits+"\n"
                else:
                    r=r + "    "+reg.fieldNameList[i]+" : "+reg.enumTypeList[i].enumName+"_enum; -- "+bits+"\n"
            else:
                r=r + "    "+reg.fieldNameList[i]+" : std_ulogic_vector("+str(reg.bitWidthList[i]-1)+" downto 0); -- "+bits+"\n"
        r=r + "  end record;\n\n"
        return r

    def returnRegistersRecordTypeString(self):
        r=""
        r=r + "  type "+self.name+"_record_type is record\n"
        for reg in self.registerList:
            r=r + '    '+reg.name+' : '+reg.name+"_record_type; -- addr "+str(int(reg.address))+"\n"
        r=r + "  end record;\n\n"                                                    
        return r     

    def returnRecToSulvFunctionString(self,reg):
        r=""
        r=r + "  function "+reg.name+"_record_type_to_sulv (v : "+reg.name+"_record_type) return std_ulogic_vector is\n"
        r=r + "    variable r : std_ulogic_vector (data_width-1 downto 0);\n"
        r=r + "  begin\n"
        r=r + "    r :=  (others => '0');\n"
        for i in reversed(range(len(reg.fieldNameList))):
            bits = str(reg.bitOffsetList[i]+reg.bitWidthList[i]-1)+" downto "+str(reg.bitOffsetList[i])
            if reg.enumTypeList[i] is not None:
                if reg.enumTypeList[i].allReadyExist==False:
                    r=r + "    r("+bits+") := "+reg.enumTypeList[i].name+"_enum_to_sulv(v."+reg.fieldNameList[i]+");\n"
                else:
                    r=r + "    r("+bits+") := "+reg.enumTypeList[i].enumName+"_enum_to_sulv(v."+reg.fieldNameList[i]+");\n"
            else:
                r=r + "    r("+bits+") := v."+reg.fieldNameList[i]+";\n"
        r=r + "    return r;\n"
        r=r + "  end function;\n\n"
        return r

    def returnSulvToRecFunctionString(self,reg):
        r=""
        r=r + "   function sulv_to_"+reg.name+"_record_type (v : std_ulogic_vector) return "+reg.name+"_record_type is\n"
        r=r + "     variable r : "+reg.name+"_record_type;\n"
        r=r + "   begin\n"
        for i in reversed(range(len(reg.fieldNameList))):
            bits = str(reg.bitOffsetList[i]+reg.bitWidthList[i]-1)+" downto "+str(reg.bitOffsetList[i])
            if reg.enumTypeList[i] is not None:
                if reg.enumTypeList[i].allReadyExist==False:
                    r=r + "    r."+reg.fieldNameList[i]+" := sulv_to_"+reg.enumTypeList[i].name+"_enum(v("+bits+"));\n"
                else:
                    r=r + "    r."+reg.fieldNameList[i]+" := sulv_to_"+reg.enumTypeList[i].enumName+"_enum(v("+bits+"));\n"
            else:
                r=r + "    r."+reg.fieldNameList[i]+" := v("+bits+");\n"
        r=r + "     return r;\n"
        r=r + "   end function;\n\n"

        return r

    def returnReadFunctionString(self):
        r=""
        r=r + "     function read_"+self.name+"(registers : "+self.name+"_record_type;\n"
        r=r + "                                 address   : std_ulogic_vector (addr_width-1 downto 0)\n"
        r=r + "                                 ) return std_ulogic_vector is\n"
        r=r + "       variable r : std_ulogic_vector (data_width-1 downto 0);\n"
        r=r + "     begin\n"
        r=r + "       case to_integer(unsigned(address)) is\n"
        for reg in self.registerList:
            r=r + "         when " + reg.name + "_addr => r:= "+reg.name+"_record_type_to_sulv(registers."+reg.name+");\n "
        r=r + "        when others    => r := (others => '0');\n"
        r=r + "       end case;\n"
        r=r + "       return r;\n"
        r=r + "     end function;\n\n"
        return r

    def returnWriteFunctionString(self):
        r=""
        r=r + "  function write_"+self.name+"(value     : std_ulogic_vector (data_width-1 downto 0);\n"
        r=r + "                               address   : std_ulogic_vector (addr_width-1 downto 0);\n"
        r=r + "                               registers : "+self.name+"_record_type\n"
        r=r + "                               ) return "+self.name+"_record_type is\n"
        r=r + "    variable r : "+self.name+"_record_type;\n"
        r=r + "  begin\n"
        r=r + "    r := registers;\n"
        r=r + "    case to_integer(unsigned(address)) is\n"
        for reg in self.registerList:
            r=r + "         when " + reg.name + "_addr => r."+reg.name+" := sulv_to_"+reg.name+"_record_type(value);\n"
        r=r + "      when others    => null;\n"
        r=r + "    end case;\n"
        r=r + "    return r;\n"
        r=r + "  end function;\n\n"
        return r

    def returnResetFunctionString(self):
        r=""
        r=r + "  function reset_"+self.name+" return "+self.name+"_record_type is\n"
        r=r + "    variable r : "+self.name+"_record_type;\n"
        r=r + "  begin\n"
        for reg in self.registerList:
            if reg.resetValue:
                r=r + "         r."+reg.name+" := sulv_to_"+reg.name+"_record_type("+reg.name+"_reset_value);\n"
        r=r + "    return r;\n"
        r=r + "  end function;\n\n"
        return r

    def returnPkgBodyString(self):
        r=""
        r=r + "package body "+self.name+"_vhd_pkg is \n\n"

        r=r + self.returnRegFieldEnumTypeStrings(False)

        for reg in self.registerList:
            r=r + self.returnRecToSulvFunctionString(reg)
            r=r + self.returnSulvToRecFunctionString(reg)

        r=r + self.returnReadFunctionString()
        r=r + self.returnWriteFunctionString()
        r=r + self.returnResetFunctionString()
        r=r + "end package body; \n"
        return r


class systemVerilogAddressBlock(addressBlockClass):


    def __init__(self, name, addrWidth, dataWidth):
        self.name = name
        self.addrWidth = addrWidth
        self.dataWidth = dataWidth
        self.registerList=[]
        self.suffix = "_sv_pkg.sv"

    def returnIncludeString(self):
        r = "\n"
        r=r + "`define "+self.name+"_addr_width "+str(self.addrWidth)+"\n"
        r=r + "`define "+self.name+"_data_width "+str(self.dataWidth)+"\n"
        return r     

    def returnSizeString(self):
        r = "\n"
        r=r + "const int addr_width = "+str(self.addrWidth)+";\n"
        r=r + "const int data_width = "+str(self.dataWidth)+";\n"
        return r     

    def returnAddressesString(self):
        r = "\n"
        for reg in self.registerList:
            r=r+"const int "+reg.name+"_addr = "+str(reg.address)+";\n"
        r=r+"\n";
        return r

    def returnAddressListString(self):
        r = "\n"
        r = "//synopsys translate_off\n"    
        r=r+"const int "+self.name+"_regAddresses ["+str(len(self.registerList))+"] = {"
        l = []
        for reg in self.registerList:
            l.append("\n     "+reg.name+"_addr")
            
        r=r+",".join(l)
        r=r+"};\n"
        r=r+"\n"
        r=r+"const string "+self.name+"_regNames ["+str(len(self.registerList))+"] = {"
        l = []
        for reg in self.registerList:
            l.append('\n      "'+reg.name+'"')            
        r=r+",".join(l)
        r=r+"};\n"
        r=r+"//synopsys translate_on\n\n"
        return r


    def enumeratedType(self,prepend,fieldName,valueNames,values):
        r = "\n"
        members = []
        # dont want to create to simple names in the global names space.
        # should preppend with name from ipxact file
        for index in range(len(valueNames)):
            name  = valueNames[index]
            value = values[index]
            members.append(name+"="+value)
        r = "typedef enum { "+",".join(members)+"} enum_"+fieldName+";\n"
        return r

    def returnResetValuesString(self):
        r = ""
        for reg in self.registerList:
            if reg.resetValue:
                r = r + "const "+reg.name+"_struct_type "+reg.name+"_reset_value = "+reg.resetValue+";\n"
        r = r + "\n"
        return r

    def returnStructString(self):
        r = "\n"
        for reg in self.registerList:
            r = r + "\ntypedef struct packed {\n"
            for i in reversed(range(len(reg.fieldNameList))):
                bits = "bits ["+str(reg.bitOffsetList[i]+reg.bitWidthList[i]-1)+":"+str(reg.bitOffsetList[i])+"]"
                r=r+"   bit ["+str(reg.bitWidthList[i]-1)+":0] "+str(reg.fieldNameList[i])+";//"+bits+"\n"
            r=r+"} "+reg.name+"_struct_type;\n\n";
        return r

    def returnRegistersStructString(self):
        r = "typedef struct packed {\n"
        for reg in self.registerList:
            r=r+"   "+reg.name+"_struct_type "+reg.name+";\n";
        r=r+"} "+self.name+"_struct_type;\n\n";
        return r

    def returnReadFunctionString(self):
        r =   "function bit [31:0] read_"+self.name+"("+self.name+"_struct_type registers,int address);\n"
        r=r+"      bit [31:0]  r;\n"
        r=r+"      case(address)\n"
        for reg in self.registerList:
            r=r+"         "+reg.name+"_addr: r = registers."+reg.name+";\n"
        r=r+"        default: r =0;\n"
        r=r+"      endcase\n"
        r=r+"      return r;\n"
        r=r+"endfunction\n\n"
        return r

    def returnWriteFunctionString(self):
        r =   "function "+self.name+"_struct_type write_"+self.name+"(bit [31:0] data, int address, \n"
        r=r+"                                        "+self.name+"_struct_type registers);\n"
        r=r+"   "+self.name+"_struct_type r = registers;\n"
        r=r+"   case(address)\n"
        for reg in self.registerList:
            r=r+"         "+reg.name+"_addr: r."+reg.name+"=data;\n"
        r=r+"   endcase // case address\n"
        r=r+"   return r;\n"
        r=r+"endfunction\n\n"
        return r

    def returnResetFunctionString(self):
        r=  "function "+self.name+"_struct_type reset_"+self.name+"();\n"
        r=r+"   "+self.name+"_struct_type r;\n"
        for reg in self.registerList:
            if reg.resetValue:
                r=r+"   r."+reg.name+"="+reg.name+"_reset_value;\n"
        r=r+"   return r;\n"
        r=r+"endfunction\n"
        r=r+"\n"
        return r;

    def returnAsString(self):
        r=''
        r = r + "package "+self.name+"_sv_pkg;\n\n";
        r = r + self.returnSizeString()
        r = r + self.returnAddressesString()
        r = r + self.returnAddressListString()
        r = r + self.returnStructString()
        r = r + self.returnResetValuesString()
        r = r + self.returnRegistersStructString()
        r = r + self.returnReadFunctionString()
        r = r + self.returnWriteFunctionString()
        r = r + self.returnResetFunctionString()
        r = r + "endpackage //"+self.name+"_sv_pkg\n";
        return r








class ipxactParser:
    def __init__(self,srcFile):
        self.srcFile=srcFile
        self.enumTypeClassRegistry = enumTypeClassRegistry()

    def returnDocument(self):
        spirit_ns = 'http://www.spiritconsortium.org/XMLSchema/SPIRIT/1.5'
        tree = etree.parse(self.srcFile)
        etree.register_namespace('spirit', spirit_ns)
        namespace = tree.getroot().tag[1:].split("}")[0]
        spiritString ='{'+spirit_ns+'}'
        docName = tree.find(spiritString+"name").text
        d = documentClass(docName)
        memoryMaps = tree.find(spiritString+"memoryMaps")
        memoryMapList = memoryMaps.findall(spiritString+"memoryMap")
        for memoryMap in memoryMapList:
            memoryMapName = memoryMap.find(spiritString+"name").text
            addressBlockList = memoryMap.findall(spiritString+"addressBlock")
            m = memoryMapClass(memoryMapName)
            for addressBlock in addressBlockList:
                addressBlockName=addressBlock.find(spiritString+"name").text
                registerList = addressBlock.findall(spiritString+"register")
                baseAddress = int(addressBlock.find(spiritString+"baseAddress").text)
                nbrOfAddresses =  int(addressBlock.find(spiritString+"range").text) #TODO, this is wrong 
                addrWidth = int(math.ceil((math.log(baseAddress+nbrOfAddresses,2))))
                dataWidth = int(addressBlock.find(spiritString+"width").text)
                a = addressBlockClass(addressBlockName,addrWidth, dataWidth)
                for registerElem in registerList:
                    regName=registerElem.find(spiritString+"name").text
                    reset=registerElem.find(spiritString+"reset")
                    if reset: 
                        resetValue=reset.find(spiritString+"value").text
                    else:
                        resetValue = None
                    desc = registerElem.find(spiritString+"description").text
                    regAddress=baseAddress+int(registerElem.find(spiritString+"addressOffset").text)
                    r = self.returnRegister(spiritString,registerElem,regAddress,resetValue,desc,dataWidth)
                    a.addRegister(r)
                m.addAddressBlock(a)
            d.addMemoryMap(m)

        return d 

    def returnRegister(self,spiritString,registerElem,regAddress,resetValue,regDesc,dataWidth):
        r = "\n"
        regName=registerElem.find(spiritString+"name").text
        fieldList = registerElem.findall(spiritString+"field")
        fieldNameList = [item.find(spiritString+"name").text for item in fieldList]
        bitOffsetList = [item.find(spiritString+"bitOffset").text for item in fieldList]
        bitWidthList = [item.find(spiritString+"bitWidth").text for item in fieldList] 
        fieldDescList = [item.find(spiritString+"description").text for item in fieldList]
        enumTypeList = []
        for index in range(len(fieldList)):
            fieldElem = fieldList[index]
            bitWidth = bitWidthList[index]
            fieldName = fieldNameList[index]
            enumeratedValuesElem = fieldElem.find(spiritString+"enumeratedValues")
            if enumeratedValuesElem is not None:
                enumeratedValueList = enumeratedValuesElem.findall(spiritString+"enumeratedValue")
                valuesNameList = [item.find(spiritString+"name").text for item in enumeratedValueList]
                valuesList = [item.find(spiritString+"value").text for item in enumeratedValueList]
                if len(valuesNameList) > 0 and int(bitWidth) > 1:
                    # dont create enums of booleans
                    # only decreases readability
                    enum = enumTypeClass(fieldName,bitWidth,valuesNameList,valuesList)
                    enum = self.enumTypeClassRegistry.allReadyExist(enum)
                    enumTypeList.append(enum)
                else:
                    enumTypeList.append(None)
            else:
                enumTypeList.append(None)

        if len(fieldNameList)==0:
            fieldNameList.append(regName)
            bitOffsetList.append(0)
            bitWidthList.append(dataWidth)
            fieldDescList.append('')
            enumTypeList.append(None)



        (regName,fieldNameList,bitOffsetList,bitWidthList,fieldDescList,enumTypeList) = sortRegisterAndFillHoles(regName,fieldNameList,bitOffsetList,bitWidthList,fieldDescList,enumTypeList)
        
        reg = registerClass(regName,regAddress,resetValue,regDesc,fieldNameList,bitOffsetList,bitWidthList,fieldDescList,enumTypeList)
        return reg

class ipxact2otherGenerator:
    def __init__(self,destDir,namingScheme="addressBlockName"):
        self.destDir=destDir  
        self.namingScheme=namingScheme

    def write(self,fileName,string):
        print "writing file "+ self.destDir+'/'+fileName
        f = open(self.destDir+'/'+fileName, 'w')
        f.write(string)

    def generate(self,generatorClass,document):
        self.document = document
        docName = document.name
        for memoryMap in document.memoryMapList:
            mapName = memoryMap.name
            for addressBlock in memoryMap.addressBlockList:
                blockName = addressBlock.name
                block = generatorClass(addressBlock.name,
                                        addressBlock.addrWidth,
                                        addressBlock.dataWidth)
                block.setRegisterList(addressBlock.registerList)
                s = block.returnAsString()
                if(self.namingScheme=="addressBlockName"):
                    fileName = blockName+block.suffix
                else:
                    fileName = docName+'_'+mapName+'_'+blockName+block.suffix

                self.write(fileName,s)
                
                if generatorClass==systemVerilogAddressBlock:
                    includeFileName = fileName+"h"
                    includeString = block.returnIncludeString()
                    self.write(includeFileName,includeString)   
