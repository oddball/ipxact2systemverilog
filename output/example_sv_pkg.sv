package example_sv_pkg;


const int addr_width = 3;
const int data_width = 32;

const int reg0_addr = 0;
const int reg1_addr = 1;
const int reg2_addr = 2;
const int reg3_addr = 3;
const int reg4_addr = 4;
const int reg5_addr = 5;
const int reg6_addr = 6;
const int reg7_addr = 7;

//synopsys translate_off
const int example_regAddresses [8] = {
     reg0_addr,
     reg1_addr,
     reg2_addr,
     reg3_addr,
     reg4_addr,
     reg5_addr,
     reg6_addr,
     reg7_addr};

const string example_regNames [8] = {
      "reg0",
      "reg1",
      "reg2",
      "reg3",
      "reg4",
      "reg5",
      "reg6",
      "reg7"};
const reg example_regUnResetedAddresses [8] = {
   0,
   0,
   0,
   0,
   0,
   1,
   1,
   1};

//synopsys translate_on



typedef struct packed {
   bit [7:0] byte3;//bits [31:24]
   bit [7:0] byte2;//bits [23:16]
   bit [7:0] byte1;//bits [15:8]
   bit [7:0] byte0;//bits [7:0]
} reg0_struct_type;


typedef struct packed {
   bit [31:0] field0;//bits [31:0]
} reg1_struct_type;


typedef struct packed {
   bit [1:0] monkey2;//bits [5:4]
   bit [1:0] monkey;//bits [3:2]
   bit [0:0] power2;//bits [1:1]
   bit [0:0] power;//bits [0:0]
} reg2_struct_type;


typedef struct packed {
   bit [31:0] field0;//bits [31:0]
} reg3_struct_type;


typedef struct packed {
   bit [31:0] reg4;//bits [31:0]
} reg4_struct_type;


typedef struct packed {
   bit [31:0] reg5;//bits [31:0]
} reg5_struct_type;


typedef struct packed {
   bit [31:0] reg6;//bits [31:0]
} reg6_struct_type;


typedef struct packed {
   bit [9:0] field1;//bits [25:16]
   bit [5:0] None;//bits [15:10]
   bit [9:0] field0;//bits [9:0]
} reg7_struct_type;

const reg0_struct_type reg0_reset_value = 0;
const reg1_struct_type reg1_reset_value = 1;
const reg2_struct_type reg2_reset_value = 1;
const reg3_struct_type reg3_reset_value = 1;
const reg4_struct_type reg4_reset_value = 12;

typedef struct packed {
   reg0_struct_type reg0;
   reg1_struct_type reg1;
   reg2_struct_type reg2;
   reg3_struct_type reg3;
   reg4_struct_type reg4;
   reg5_struct_type reg5;
   reg6_struct_type reg6;
   reg7_struct_type reg7;
} example_struct_type;

function bit [31:0] read_example(example_struct_type registers,int address);
      bit [31:0]  r;
      case(address)
         reg0_addr: r = registers.reg0;
         reg1_addr: r = registers.reg1;
         reg2_addr: r = registers.reg2;
         reg3_addr: r = registers.reg3;
         reg4_addr: r = registers.reg4;
         reg5_addr: r = registers.reg5;
         reg6_addr: r = registers.reg6;
         reg7_addr: r = registers.reg7;
        default: r =0;
      endcase
      return r;
endfunction

function example_struct_type write_example(bit [31:0] data, int address, 
                                        example_struct_type registers);
   example_struct_type r = registers;
   case(address)
         reg0_addr: r.reg0=data;
         reg1_addr: r.reg1=data;
         reg2_addr: r.reg2=data;
         reg3_addr: r.reg3=data;
         reg4_addr: r.reg4=data;
         reg5_addr: r.reg5=data;
         reg6_addr: r.reg6=data;
         reg7_addr: r.reg7=data;
   endcase // case address
   return r;
endfunction

function example_struct_type reset_example();
   example_struct_type r;
   r.reg0=reg0_reset_value;
   r.reg1=reg1_reset_value;
   r.reg2=reg2_reset_value;
   r.reg3=reg3_reset_value;
   r.reg4=reg4_reset_value;
   return r;
endfunction

endpackage //example_sv_pkg
