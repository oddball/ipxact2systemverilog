// Automatically generated
// with the command 'bin/ipxact2systemverilog --srcFile example/input/test2.xml --destDir example/output'
//
// Do not manually edit!
//
package example2_sv_pkg;


const int addr_width = 2;
const int data_width = 8;

const int reg0_addr = 0;
const int reg1_addr = 1;

//synopsys translate_off
const int example2_regAddresses [2] = '{
     reg0_addr,
     reg1_addr};

const string example2_regNames [2] = '{
      "reg0",
      "reg1"};
const reg example2_regUnResetedAddresses [2] = '{
   1'b1,
   1'b1};

//synopsys translate_on



typedef struct packed {
   bit [5:0] field1;//bits [7:2]
   bit [1:0] field0;//bits [1:0]
} reg0_struct_type;


typedef struct packed {
   bit [7:0] field0;//bits [7:0]
} reg1_struct_type;


typedef struct packed {
   reg0_struct_type reg0;
   reg1_struct_type reg1;
} example2_struct_type;

function bit [31:0] read_example2(example2_struct_type registers,int address);
      bit [31:0]  r;
      case(address)
         reg0_addr: r[$bits(registers.reg0)-1:0] = registers.reg0;
         reg1_addr: r[$bits(registers.reg1)-1:0] = registers.reg1;
        default: r =0;
      endcase
      return r;
endfunction

function example2_struct_type write_example2(bit [31:0] data, int address,
                                             example2_struct_type registers);
   example2_struct_type r;
   r = registers;
   case(address)
         reg0_addr: r.reg0 = data[$bits(registers.reg0)-1:0];
         reg1_addr: r.reg1 = data[$bits(registers.reg1)-1:0];
   endcase // case address
   return r;
endfunction

function example2_struct_type reset_example2();
   example2_struct_type r;
   return r;
endfunction

endpackage //example2_sv_pkg
