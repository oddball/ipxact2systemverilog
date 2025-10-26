--
-- Automatically generated
-- with the command 'ipxact2vhdl --srcFile example/input/test2.xml --destDir example/output'
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


  -- samename
  type samename_enum is (a,  -- a
                         b,  -- b
                         c,  -- c
                         d);  -- d
  function samename_enum_to_sulv(v: samename_enum) return std_ulogic_vector;
  function sulv_to_samename_enum(v: std_ulogic_vector(2-1 downto 0)) return samename_enum;


  constant reg0_addr : natural := 0;  -- 0x0
  constant reg1_addr : natural := 1;  -- 0x1
  constant samename_addr : natural := 29;  -- 0x1d

  constant samename_reset_value : std_ulogic_vector(data_width-1 downto 0) := std_ulogic_vector(to_unsigned(0, data_width));  -- 0x00


  type reg0_record_type is record
    field1 : std_ulogic_vector(5 downto 0); -- [7:2]
    field0 : std_ulogic_vector(1 downto 0); -- [1:0]
  end record;

  type reg1_record_type is record
    field0 : std_ulogic_vector(7 downto 0); -- [7:0], Min: 0x00, Max: 0x07
  end record;

  type samename_record_type is record
    unused0 : std_ulogic_vector(5 downto 0); -- [7:2]
    samename : samename_enum; -- [1:0]
  end record;

  type example2_in_record_type is record
    reg0 : reg0_record_type; -- addr 0x0
    reg1 : reg1_record_type; -- addr 0x1
    samename : samename_record_type; -- addr 0x1d
  end record;

  function read_example2(registers_i : example2_in_record_type;
                         address : std_ulogic_vector(addr_width-1 downto 0)
                         ) return std_ulogic_vector;

end;


package body example2_vhd_pkg is

  -- samename
  function samename_enum_to_sulv(v: samename_enum) return std_ulogic_vector is
    variable r : std_ulogic_vector(2-1 downto 0);
  begin
       case v is
         when a => r:="00"; -- 0
         when b => r:="01"; -- 1
         when c => r:="10"; -- 2
         when d => r:="11"; -- 3
       end case;
    return r;
  end function;

  function sulv_to_samename_enum(v: std_ulogic_vector(2-1 downto 0)) return samename_enum is
    variable r : samename_enum;
  begin
       case v is
         when "00" => r:=a;
         when "01" => r:=b;
         when "10" => r:=c;
         when "11" => r:=d;
         when others => r:=a; -- error
       end case;
    return r;
  end function;

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

  function samename_record_type_to_sulv(v : samename_record_type) return std_ulogic_vector is
    variable r : std_ulogic_vector(data_width-1 downto 0);
  begin
    r :=  (others => '0');
    r(7 downto 2) := v.unused0;
    r(1 downto 0) := samename_enum_to_sulv(v.samename);
    return r;
  end function;

  function sulv_to_samename_record_type(v : std_ulogic_vector) return samename_record_type is
    variable r : samename_record_type;
  begin
    r.unused0 := v(7 downto 2);
    r.samename := sulv_to_samename_enum(v(1 downto 0));
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
      when samename_addr => r:= samename_record_type_to_sulv(registers_i.samename);
      when others => r := (others => '0');
    end case;
    return r;
  end function;

end package body;
