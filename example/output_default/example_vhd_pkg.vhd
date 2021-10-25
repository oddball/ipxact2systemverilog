--
-- Automatically generated
-- with the command 'bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output_default --config example/input/default.ini'
--
-- Do not manually edit!
--
-- VHDL 93
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package example_vhd_pkg is

  constant addr_width : natural := 3;
  constant data_width : natural := 32;


  -- monkey
  type monkey_enum is (chimp,  -- a monkey
                       gorilla,
                       phb);  -- and another monkey
  function monkey_enum_to_sulv(v: monkey_enum ) return std_ulogic_vector;
  function sulv_to_monkey_enum(v: std_ulogic_vector(2-1 downto 0)) return monkey_enum;


  constant reg0_addr : natural := 0 ;  -- 0x0
  constant reg1_addr : natural := 1 ;  -- 0x1
  constant reg2_addr : natural := 2 ;  -- 0x2
  constant reg3_addr : natural := 3 ;  -- 0x3
  constant reg4_addr : natural := 4 ;  -- 0x4
  constant reg5_addr : natural := 5 ;  -- 0x5
  constant reg6_addr : natural := 6 ;  -- 0x6
  constant reg7_addr : natural := 7 ;  -- 0x7

  constant reg0_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(0, data_width));  -- 0x00000000
  constant reg1_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(1, data_width));  -- 0x00000001
  constant reg2_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(1, data_width));  -- 0x00000001
  constant reg3_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(1, data_width));  -- 0x00000001
  constant reg4_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(12, data_width));  -- 0x0000000c
  constant reg7_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(0, data_width));  -- 0x00000000


  type reg0_record_type is record
    byte3 : std_ulogic_vector(7 downto 0); -- [31:24]
    byte2 : std_ulogic_vector(7 downto 0); -- [23:16]
    byte1 : std_ulogic_vector(7 downto 0); -- [15:8]
    byte0 : std_ulogic_vector(7 downto 0); -- [7:0]
  end record;

  type reg1_record_type is record
    field0 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg2_record_type is record
    monkey2 : monkey_enum; -- [5:4]
    monkey : monkey_enum; -- [3:2]
    power2 : std_ulogic; -- [1]
    power : std_ulogic; -- [0]
  end record;

  type reg3_record_type is record
    field0 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg4_record_type is record
    reg4 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg5_record_type is record
    reg5 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg6_record_type is record
    reg6 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg7_record_type is record
    nibble2 : std_ulogic_vector(3 downto 0); -- [19:16]
    unused1 : std_ulogic_vector(3 downto 0); -- [15:12]
    nibble1 : std_ulogic_vector(3 downto 0); -- [11:8]
    unused0 : std_ulogic_vector(3 downto 0); -- [7:4]
    nibble0 : std_ulogic_vector(3 downto 0); -- [3:0]
  end record;

  type example_in_record_type is record
    reg6 : reg6_record_type; -- addr 0x6
  end record;

  type example_out_record_type is record
    reg0 : reg0_record_type; -- addr 0x0
    reg1 : reg1_record_type; -- addr 0x1
    reg2 : reg2_record_type; -- addr 0x2
    reg3 : reg3_record_type; -- addr 0x3
    reg4 : reg4_record_type; -- addr 0x4
    reg5 : reg5_record_type; -- addr 0x5
    reg7 : reg7_record_type; -- addr 0x7
  end record;

  function read_example(registers_i : example_in_record_type;
                        registers_o : example_out_record_type;
                        address : std_ulogic_vector(addr_width-1 downto 0)
                        ) return std_ulogic_vector;

  function write_example(value : std_ulogic_vector(data_width-1 downto 0);
                         address : std_ulogic_vector(addr_width-1 downto 0);
                         registers_o : example_out_record_type
                         ) return example_out_record_type;

  function reset_example return example_out_record_type;
  function reset_example(address: std_ulogic_vector(addr_width-1 downto 0));
                         registers_o : example_out_record_type
                         ) return example_out_record_type;

end;


package body example_vhd_pkg is

  -- monkey
  function monkey_enum_to_sulv(v: monkey_enum ) return std_ulogic_vector is
    variable r : std_ulogic_vector(2-1 downto 0);
  begin
       case v is
         when chimp => r:="00"; -- 0
         when gorilla => r:="01"; -- 1
         when phb => r:="10"; -- 2
       end case;
    return r;
  end function;

  function sulv_to_monkey_enum(v: std_ulogic_vector(2-1 downto 0)) return monkey_enum is
    variable r : monkey_enum;
  begin
       case v is
         when "00" => r:=chimp;
         when "01" => r:=gorilla;
         when "10" => r:=phb;
         when others => r:=chimp; -- error
       end case;
    return r;
  end function;

  function reg0_record_type_to_sulv(v : reg0_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 24) := v.byte3;
    r(23 downto 16) := v.byte2;
    r(15 downto 8) := v.byte1;
    r(7 downto 0) := v.byte0;
    return r;
  end function;

  function sulv_to_reg0_record_type(v : std_ulogic_vector) return reg0_record_type is
    variable r : reg0_record_type;
  begin
    r.byte3 := v(31 downto 24);
    r.byte2 := v(23 downto 16);
    r.byte1 := v(15 downto 8);
    r.byte0 := v(7 downto 0);
    return r;
  end function;

  function reg1_record_type_to_sulv(v : reg1_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) := v.field0;
    return r;
  end function;

  function sulv_to_reg1_record_type(v : std_ulogic_vector) return reg1_record_type is
    variable r : reg1_record_type;
  begin
    r.field0 := v(31 downto 0);
    return r;
  end function;

  function reg2_record_type_to_sulv(v : reg2_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(5 downto 4) := monkey_enum_to_sulv(v.monkey2);
    r(3 downto 2) := monkey_enum_to_sulv(v.monkey);
    r(1) := v.power2;
    r(0) := v.power;
    return r;
  end function;

  function sulv_to_reg2_record_type(v : std_ulogic_vector) return reg2_record_type is
    variable r : reg2_record_type;
  begin
    r.monkey2 := sulv_to_monkey_enum(v(5 downto 4));
    r.monkey := sulv_to_monkey_enum(v(3 downto 2));
    r.power2 := v(1);
    r.power := v(0);
    return r;
  end function;

  function reg3_record_type_to_sulv(v : reg3_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) := v.field0;
    return r;
  end function;

  function sulv_to_reg3_record_type(v : std_ulogic_vector) return reg3_record_type is
    variable r : reg3_record_type;
  begin
    r.field0 := v(31 downto 0);
    return r;
  end function;

  function reg4_record_type_to_sulv(v : reg4_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) := v.reg4;
    return r;
  end function;

  function sulv_to_reg4_record_type(v : std_ulogic_vector) return reg4_record_type is
    variable r : reg4_record_type;
  begin
    r.reg4 := v(31 downto 0);
    return r;
  end function;

  function reg5_record_type_to_sulv(v : reg5_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) := v.reg5;
    return r;
  end function;

  function sulv_to_reg5_record_type(v : std_ulogic_vector) return reg5_record_type is
    variable r : reg5_record_type;
  begin
    r.reg5 := v(31 downto 0);
    return r;
  end function;

  function reg6_record_type_to_sulv(v : reg6_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) := v.reg6;
    return r;
  end function;

  function sulv_to_reg6_record_type(v : std_ulogic_vector) return reg6_record_type is
    variable r : reg6_record_type;
  begin
    r.reg6 := v(31 downto 0);
    return r;
  end function;

  function reg7_record_type_to_sulv(v : reg7_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(19 downto 16) := v.nibble2;
    r(15 downto 12) := v.unused1;
    r(11 downto 8) := v.nibble1;
    r(7 downto 4) := v.unused0;
    r(3 downto 0) := v.nibble0;
    return r;
  end function;

  function sulv_to_reg7_record_type(v : std_ulogic_vector) return reg7_record_type is
    variable r : reg7_record_type;
  begin
    r.nibble2 := v(19 downto 16);
    r.unused1 := v(15 downto 12);
    r.nibble1 := v(11 downto 8);
    r.unused0 := v(7 downto 4);
    r.nibble0 := v(3 downto 0);
    return r;
  end function;

  function read_example(registers_i : example_in_record_type;
                        registers_o : example_out_record_type;
                        address : std_ulogic_vector(addr_width-1 downto 0)
                        ) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    case to_integer(unsigned(address)) is
      when reg0_addr => r:= reg0_record_type_to_sulv(registers_o.reg0);
      when reg1_addr => r:= reg1_record_type_to_sulv(registers_o.reg1);
      when reg2_addr => r:= reg2_record_type_to_sulv(registers_o.reg2);
      when reg3_addr => r:= reg3_record_type_to_sulv(registers_o.reg3);
      when reg4_addr => r:= reg4_record_type_to_sulv(registers_o.reg4);
      when reg5_addr => r:= reg5_record_type_to_sulv(registers_o.reg5);
      when reg6_addr => r:= reg6_record_type_to_sulv(registers_i.reg6);
      when reg7_addr => r:= reg7_record_type_to_sulv(registers_o.reg7);
      when others => r := (others => '0');
    end case;
    return r;
  end function;

  function write_example(value : std_ulogic_vector(data_width-1 downto 0);
                         address : std_ulogic_vector(addr_width-1 downto 0);
                         registers_o : example_out_record_type
                         ) return example_out_record_type is
    variable r : example_out_record_type;
  begin
    r := registers_o;
    case to_integer(unsigned(address)) is
         when reg0_addr => r.reg0 := sulv_to_reg0_record_type(value);
         when reg1_addr => r.reg1 := sulv_to_reg1_record_type(value);
         when reg2_addr => r.reg2 := sulv_to_reg2_record_type(value);
         when reg3_addr => r.reg3 := sulv_to_reg3_record_type(value);
         when reg4_addr => r.reg4 := sulv_to_reg4_record_type(value);
         when reg5_addr => r.reg5 := sulv_to_reg5_record_type(value);
         when reg7_addr => r.reg7 := sulv_to_reg7_record_type(value);
      when others => null;
    end case;
    return r;
  end function;

  function reset_example return example_out_record_type is
    variable r : example_out_record_type;
  begin
         r.reg0 := sulv_to_reg0_record_type(reg0_reset_value);
         r.reg1 := sulv_to_reg1_record_type(reg1_reset_value);
         r.reg2 := sulv_to_reg2_record_type(reg2_reset_value);
         r.reg3 := sulv_to_reg3_record_type(reg3_reset_value);
         r.reg4 := sulv_to_reg4_record_type(reg4_reset_value);
         r.reg7 := sulv_to_reg7_record_type(reg7_reset_value);
    return r;
  end function;

  function reset_example(address: std_ulogic_vector(addr_width-1 downto 0);
                         registers_o : example_out_record_type
                         ) return example_out_record_type is
    variable r : example_out_record_type;
  begin
    r := registers_o;
    case to_integer(unsigned(address)) is
         when reg0_addr => r.reg0 := sulv_to_reg0_record_type(reg0_reset_value);
         when reg1_addr => r.reg1 := sulv_to_reg1_record_type(reg1_reset_value);
         when reg2_addr => r.reg2 := sulv_to_reg2_record_type(reg2_reset_value);
         when reg3_addr => r.reg3 := sulv_to_reg3_record_type(reg3_reset_value);
         when reg4_addr => r.reg4 := sulv_to_reg4_record_type(reg4_reset_value);
         when reg5_addr => r.reg5 := sulv_to_reg5_record_type(reg5_reset_value);
         when reg7_addr => r.reg7 := sulv_to_reg7_record_type(reg7_reset_value);
      when others => null;
    end case;
    return r;
  end function;

end package body;
