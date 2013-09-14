-- VHDL 93
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package example_vhd_pkg is
  constant addr_width : natural := 3;
  constant data_width : natural := 32;
 constant reg0_addr : natural := 0;
 constant reg1_addr : natural := 1;
 constant reg2_addr : natural := 2;
 constant reg3_addr : natural := 3;
 constant reg4_addr : natural := 4;
 constant reg0_reset_value : std_ulogic_vector (data_width-1 downto 0) := std_ulogic_vector( to_unsigned(0, data_width ));
 constant reg1_reset_value : std_ulogic_vector (data_width-1 downto 0) := std_ulogic_vector( to_unsigned(1, data_width ));
 constant reg2_reset_value : std_ulogic_vector (data_width-1 downto 0) := std_ulogic_vector( to_unsigned(1, data_width ));
 constant reg3_reset_value : std_ulogic_vector (data_width-1 downto 0) := std_ulogic_vector( to_unsigned(1, data_width ));
 constant reg4_reset_value : std_ulogic_vector (data_width-1 downto 0) := std_ulogic_vector( to_unsigned(12, data_width ));


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
    monkey : std_ulogic_vector(1 downto 0); -- [2:1]
    field0 : std_ulogic_vector(0 downto 0); -- [0:0]
  end record;

  type reg3_record_type is record
    field0 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type reg4_record_type is record
    reg4 : std_ulogic_vector(31 downto 0); -- [31:0]
  end record;

  type example_record_type is record
    reg0 : reg0_record_type; -- addr 0
    reg1 : reg1_record_type; -- addr 1
    reg2 : reg2_record_type; -- addr 2
    reg3 : reg3_record_type; -- addr 3
    reg4 : reg4_record_type; -- addr 4
  end record;

  function read_example(registers : example_record_type;
                        address   : std_ulogic_vector (addr_width-1 downto 0)
                        ) return std_ulogic_vector;

  function write_example(value     : std_ulogic_vector (data_width-1 downto 0);
                         address   : std_ulogic_vector (addr_width-1 downto 0);
                         registers : example_record_type
                         ) return example_record_type;

  function reset_example return example_record_type;

end;
package body example_vhd_pkg is 

  function reg0_record_type_to_sulv (v : reg0_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector (data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) :=  v.byte3 & v.byte2 & v.byte1 & v.byte0;
    return r;
  end function;

   function sulv_to_reg0_record_type (v : std_ulogic_vector) return reg0_record_type is
     variable r : reg0_record_type;
   begin
    r.byte3 := v(31 downto 24);
    r.byte2 := v(23 downto 16);
    r.byte1 := v(15 downto 8);
    r.byte0 := v(7 downto 0);
     return r;
   end function;

  function reg1_record_type_to_sulv (v : reg1_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector (data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) :=  v.field0;
    return r;
  end function;

   function sulv_to_reg1_record_type (v : std_ulogic_vector) return reg1_record_type is
     variable r : reg1_record_type;
   begin
    r.field0 := v(31 downto 0);
     return r;
   end function;

  function reg2_record_type_to_sulv (v : reg2_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector (data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(2 downto 0) :=  v.monkey & v.field0;
    return r;
  end function;

   function sulv_to_reg2_record_type (v : std_ulogic_vector) return reg2_record_type is
     variable r : reg2_record_type;
   begin
    r.monkey := v(2 downto 1);
    r.field0 := v(0 downto 0);
     return r;
   end function;

  function reg3_record_type_to_sulv (v : reg3_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector (data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) :=  v.field0;
    return r;
  end function;

   function sulv_to_reg3_record_type (v : std_ulogic_vector) return reg3_record_type is
     variable r : reg3_record_type;
   begin
    r.field0 := v(31 downto 0);
     return r;
   end function;

  function reg4_record_type_to_sulv (v : reg4_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector (data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(31 downto 0) :=  v.reg4;
    return r;
  end function;

   function sulv_to_reg4_record_type (v : std_ulogic_vector) return reg4_record_type is
     variable r : reg4_record_type;
   begin
    r.reg4 := v(31 downto 0);
     return r;
   end function;

     function read_example(registers : example_record_type;
                                 address   : std_ulogic_vector (addr_width-1 downto 0)
                                 ) return std_ulogic_vector is
       variable r : std_ulogic_vector (data_width-1 downto 0);
     begin
       case to_integer(unsigned(address)) is
         when reg0_addr => r:= reg0_record_type_to_sulv(registers.reg0);
          when reg1_addr => r:= reg1_record_type_to_sulv(registers.reg1);
          when reg2_addr => r:= reg2_record_type_to_sulv(registers.reg2);
          when reg3_addr => r:= reg3_record_type_to_sulv(registers.reg3);
          when reg4_addr => r:= reg4_record_type_to_sulv(registers.reg4);
         when others    => r := (others => '0');
       end case;
       return r;
     end function;

  function write_example(value     : std_ulogic_vector (data_width-1 downto 0);
                               address   : std_ulogic_vector (addr_width-1 downto 0);
                               registers : example_record_type
                               ) return example_record_type is
    variable r : example_record_type;
  begin
    r := registers;
    case to_integer(unsigned(address)) is
         when reg0_addr => r.reg0 := sulv_to_reg0_record_type(value);
         when reg1_addr => r.reg1 := sulv_to_reg1_record_type(value);
         when reg2_addr => r.reg2 := sulv_to_reg2_record_type(value);
         when reg3_addr => r.reg3 := sulv_to_reg3_record_type(value);
         when reg4_addr => r.reg4 := sulv_to_reg4_record_type(value);
      when others    => null;
    end case;
    return r;
  end function;

  function reset_example return example_record_type is
    variable r : example_record_type;
  begin
         r.reg0 := sulv_to_reg0_record_type(reg0_reset_value);
         r.reg1 := sulv_to_reg1_record_type(reg1_reset_value);
         r.reg2 := sulv_to_reg2_record_type(reg2_reset_value);
         r.reg3 := sulv_to_reg3_record_type(reg3_reset_value);
         r.reg4 := sulv_to_reg4_record_type(reg4_reset_value);
    return r;
  end function;

end package body; 
