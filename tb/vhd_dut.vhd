-- VHDL 93
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


use work.example_vhd_pkg.all;

entity vhd_dut is
  generic (
    width        : integer := 8;
    addressWidth : integer := 8
    );
  port (
    address     : in  std_ulogic_vector(addressWidth-1 downto 0);
    writeEnable : in  std_ulogic;
    writeData   : in  std_ulogic_vector(width-1 downto 0);
    readEnable  : in  std_ulogic;
    readData    : out std_ulogic_vector(width-1 downto 0);
    clk         : in  std_ulogic;
    rstn        : in  std_ulogic;
    registers_o : out example_record_type);

end vhd_dut;


architecture rtl of vhd_dut is
  signal registers : example_record_type;
begin


  process(clk, rstn)
  begin
    if rstn = '0' then
      registers <= reset_example;
      readData  <= (others => '0');
    elsif (clk = '1' and clk'event) then
      if readEnable = '1' then
        readData <= read_example(registers, address);
      elsif writeEnable = '1' then
        registers <= write_example(writeData, address, registers);
      end if;
      -- If the design, as oppose of the CPU, wants to change the register values,
      -- add code for it here.
    end if;
  end process;

  registers_o <= registers;
  

end rtl;
