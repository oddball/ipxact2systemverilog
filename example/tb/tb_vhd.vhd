-- VHDL test bench equivalent of tb.sv
-- Timescale equivalent: 1 ns/1 ps precision

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

use work.example_vhd_pkg.all;

entity tb_vhd is  
end tb_vhd;


architecture behavioral of tb_vhd is

  -- Constants equivalent to SystemVerilog parameters
  constant width : natural := data_width;
  constant addressWidth : natural := addr_width;

  -- Signals for VHDL DUT interface
  signal vhd_writeEnable : std_ulogic;
  signal vhd_writeData : std_ulogic_vector(width-1 downto 0);
  signal vhd_address : std_ulogic_vector(addressWidth-1 downto 0);
  signal vhd_readEnable : std_ulogic;
  signal vhd_readData : std_ulogic_vector(width-1 downto 0);
  signal vhd_rstn : std_ulogic;
  signal clk : std_ulogic;

  -- Register structures
  signal reset_registers : example_out_record_type;
  signal registers_i : example_in_record_type;
  signal registers_o : example_out_record_type;

  -- Arrays equivalent to SystemVerilog arrays
  type reg_address_array is array (0 to 8) of natural;
  type reg_name_array is array (0 to 8) of string(1 to 4);
  type reg_unreset_array is array (0 to 8) of std_ulogic;

  constant example_regAddresses : reg_address_array := (
    reg0_addr, reg1_addr, reg2_addr, reg3_addr, reg4_addr,
    reg5_addr, reg6_addr, reg7_addr, reg8_addr
  );

  constant example_regNames : reg_name_array := (
    "reg0", "reg1", "reg2", "reg3", "reg4",
    "reg5", "reg6", "reg7", "reg8"
  );

  constant example_regUnResetedAddresses : reg_unreset_array := (
    '0', '0', '0', '0', '0', '1', '1', '0', '0'
  );

  -- Component declarations
  component vhd_dut is
    generic (
      width : integer := 8;
      addressWidth : integer := 8
    );
    port (
      address : in std_ulogic_vector(addressWidth-1 downto 0);
      writeEnable : in std_ulogic;
      writeData : in std_ulogic_vector(width-1 downto 0);
      readEnable : in std_ulogic;
      readData : out std_ulogic_vector(width-1 downto 0);
      clk : in std_ulogic;
      rstn : in std_ulogic;
      registers_i : in example_in_record_type;
      registers_o : out example_out_record_type
    );
  end component;

begin

  -- Clock generation process
  clock_gen : process
  begin
    clk <= '0';
    wait for 5 ns;
    clk <= '1';
    wait for 5 ns;
  end process;

  -- VHDL DUT instantiation
  vhd_dut_inst : vhd_dut
    generic map (
      width => width,
      addressWidth => addressWidth
    )
    port map (
      address => vhd_address,
      writeEnable => vhd_writeEnable,
      writeData => vhd_writeData,
      readEnable => vhd_readEnable,
      readData => vhd_readData,
      clk => clk,
      rstn => vhd_rstn,
      registers_i => registers_i,
      registers_o => registers_o
    );

  -- Main test process
  test_process : process
    variable r : std_ulogic_vector(width-1 downto 0);
    variable w : std_ulogic_vector(width-1 downto 0);
    variable expected_value : std_ulogic_vector(width-1 downto 0);
    variable test_passed : boolean;
    variable temp_addr : std_ulogic_vector(addressWidth-1 downto 0);

    -- Simple function to convert std_ulogic_vector to string representation
    function to_string(vec : std_ulogic_vector) return string is
    begin
      return integer'image(to_integer(unsigned(vec)));
    end function;

    -- Reset procedure for VHDL DUT
    procedure reset_vhd_dut is
    begin
      vhd_writeEnable <= '0';
      vhd_writeData <= (others => '0');
      vhd_address <= (others => '0');
      vhd_readEnable <= '0';
      vhd_rstn <= '0';
      
      -- Wait for 3 clock cycles
      wait until rising_edge(clk);
      wait until rising_edge(clk);
      wait until rising_edge(clk);
      
      vhd_rstn <= '1';
    end procedure;

    -- Read procedure for VHDL DUT
    procedure read_vhd_dut(
      variable data : out std_ulogic_vector(width-1 downto 0);
      variable addr : in std_ulogic_vector(addressWidth-1 downto 0)
    ) is
    begin
      vhd_address <= addr;
      vhd_writeEnable <= '0';
      vhd_writeData <= (others => '0');
      vhd_readEnable <= '1';
      
      wait until rising_edge(clk);
      wait for 1 ns;
      
      data := vhd_readData;
      vhd_readEnable <= '0';
    end procedure;

    -- Write procedure for VHDL DUT
    procedure write_vhd_dut(
      variable data : in std_ulogic_vector(width-1 downto 0);
      variable addr : in std_ulogic_vector(addressWidth-1 downto 0)
    ) is
    begin
      vhd_address <= addr;
      vhd_writeEnable <= '1';
      vhd_writeData <= data;
      vhd_readEnable <= '0';
      
      wait until rising_edge(clk);
    end procedure;

    -- Test procedure for VHDL DUT
    procedure test_vhd_dut is
    begin
      -- Reset the DUT
      reset_vhd_dut;
      
      report "Test reset values for VHDL DUT" severity note;
      reset_registers <= reset_example;
      
      -- Test each register
      for j in 0 to 8 loop
        report "index = " & integer'image(j) & ", name = " & example_regNames(j) & 
               ", address = " & to_string(std_ulogic_vector(to_unsigned(example_regAddresses(j), addressWidth))) severity note;
        
        -- Read register value
        temp_addr := std_ulogic_vector(to_unsigned(example_regAddresses(j), addressWidth));
        read_vhd_dut(r, temp_addr);
        
        if example_regUnResetedAddresses(j) = '0' then
          expected_value := read_example(registers_i, reset_registers, 
                                       std_ulogic_vector(to_unsigned(example_regAddresses(j), addressWidth)));
          
          if r = expected_value then
            report "Read value = " & to_string(r) & ". OK!" severity note;
          else
            report "ERROR: Read " & to_string(r) & ", expected " & to_string(expected_value) & 
                   " at time " & time'image(now) severity error;
          end if;
        else
          report "UnResetedAddress, not comparing expected to read value!" severity note;
        end if;
      end loop;
      
      -- Wait additional clock cycles
      wait for 50 ns;
    end procedure;

  begin
    -- Initialize signals
    vhd_writeEnable <= '0';
    vhd_writeData <= (others => '0');
    vhd_address <= (others => '0');
    vhd_readEnable <= '0';
    vhd_rstn <= '0';
    registers_i <= (reg6 => (reg6 => (others => '0')));

    -- Wait for initial clock cycles
    wait for 20 ns;

    -- Test VHDL DUT
    report "Testing VHDL DUT" severity note;
    test_vhd_dut;

    -- Finish simulation
    wait for 100 ns;
    report "Simulation completed successfully!" severity note;
    std.env.finish;
  end process;

end architecture behavioral;
