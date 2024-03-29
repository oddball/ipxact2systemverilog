--
-- Automatically generated
-- with the command 'bin/ipxact2vhdl --srcFile example/input/test2.xml --destDir example/output'
--
-- Do not manually edit!
--
-- VHDL 93
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package example2_vhd_pkg is

  constant addr_width : natural := 2;
  constant data_width : natural := 8;



  constant reg0_addr : natural := 0 ;  -- 0x0
  constant reg1_addr : natural := 1 ;  -- 0x1



  type reg0_record_type is record
    field1 : std_ulogic_vector(5 downto 0); -- [7:2]
    field0 : std_ulogic_vector(1 downto 0); -- [1:0]
  end record;

  type reg1_record_type is record
    field0 : std_ulogic_vector(7 downto 0); -- [7:0]
  end record;

  type example2_in_record_type is record
    reg0 : reg0_record_type; -- addr 0x0
    reg1 : reg1_record_type; -- addr 0x1
  end record;

  function read_example2(registers_i : example2_in_record_type;
                         address : std_ulogic_vector(addr_width-1 downto 0)
                         ) return std_ulogic_vector;

end;


package body example2_vhd_pkg is

  function reg0_record_type_to_sulv(v : reg0_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(7 downto 2) := v.field1;
    r(1 downto 0) := v.field0;
    return r;
  end function;

  function sulv_to_reg0_record_type(v : std_ulogic_vector) return reg0_record_type is
    variable r : reg0_record_type;
  begin
    r.field1 := v(7 downto 2);
    r.field0 := v(1 downto 0);
    return r;
  end function;

  function reg1_record_type_to_sulv(v : reg1_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(7 downto 0) := v.field0;
    return r;
  end function;

  function sulv_to_reg1_record_type(v : std_ulogic_vector) return reg1_record_type is
    variable r : reg1_record_type;
  begin
    r.field0 := v(7 downto 0);
    return r;
  end function;

  function read_example2(registers_i : example2_in_record_type;
                         address : std_ulogic_vector(addr_width-1 downto 0)
                         ) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    case to_integer(unsigned(address)) is
      when reg0_addr => r:= reg0_record_type_to_sulv(registers_i.reg0);
      when reg1_addr => r:= reg1_record_type_to_sulv(registers_i.reg1);
      when others => r := (others => '0');
    end case;
    return r;
  end function;

end package body;
