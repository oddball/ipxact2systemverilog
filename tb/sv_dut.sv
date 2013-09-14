`timescale 1 ns/1 ps

import example_sv_pkg::*;

// This module (sv_dut) is just an example of how to use the generated package in
// a synthesizeable register bank.
module sv_dut#(
	    parameter		   width       = 8,
	    parameter		   addressWidth =8
	    )(
	      input reg [addressWidth-1:0] address,
	      input reg 		   writeEnable,
	      input reg [width-1:0] 	   writeData,
	      input reg 		   readEnable,
	      output reg [width-1:0] 	   readData,
	      input reg 		   clk,
	      input reg 		   rstn,
	      output 			   example_struct_type registers
	      );
   
   
   
   always@(posedge clk or negedge rstn)
     begin
	if(rstn==0)
	  begin
	     registers <= reset_example();
	     readData <= 0;
	  end
	else
	  begin	     
	     if(readEnable)
	       begin
		  readData <= read_example(registers,address);
	       end
	     else if(writeEnable)
	       begin
		  registers <= write_example(writeData,address,registers);		  
	       end
	     // If the design, as oppose of the CPU, wants to change the register values,
	     // add code for it here.
	  end
     end
   
endmodule