
ifneq ($(wildcard vmakefile),)
include vmakefile
endif

XSD_DIR = schema1.5

UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
SVPARSER := ./tools/linux/depmapDebug
else
SVPARSER := ./tools/osx/slang-depmap
endif



all: gen

gen: 
	bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output
	rst2html5.py example/output/example.rst example/output/example.html
	rst2pdf example/output/example.rst -o example/output/example.pdf
	pandoc -s example/output/example.rst -o example/output/example.rtf
	pandoc -s example/output/example.rst -o example/output/example.docx

both_python_versions:
	python2.7 bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output
	python2.7 bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output
	python2.7 bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output
	python3 bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output
	python3 bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output
	python3 bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output

compile: 
	test -d work || vlib work
	vlog  +incdir+example/output  example/output/example_sv_pkg.sv example/tb/sv_dut.sv example/tb/tb.sv
	vcom -93 example/output/*.vhd example/tb/vhd_dut.vhd
	vmake work > vmakefile

compile_ghdl:
	ghdl -a example/output/*.vhd example/tb/vhd_dut.vhd
	ghdl -e vhd_dut
	ghdl -r vhd_dut

compile_icarus:
	iverilog -g2012 -o foo example/output/*.sv

parse_systemverilog:
	$(SVPARSER) example/output/

.PHONY: whole_library example/output

sim: whole_library
	vsim tb -novopt -c -do "run -all; quit -force"

gui: whole_library
	vsim tb -novopt -debugDB -do "add log -r /*; run -all;"

indent:
	emacs -batch -l ~/.emacs example/output/*.sv example/tb/*.sv -f verilog-batch-indent
	emacs -batch -l ~/.emacs example/output/*.vhd -f vhdl-beautify-buffer

clean:
	rm -rf work transcript vsim.wlf vmakefile vsim.dbg
	rm -rf vhd_dut *.o *.cf

validate:
	xmllint --noout --schema ipxact2systemverilog/xml/component.xsd  example/input/test.xml

