
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
        # no config
	bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2md --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2md --srcFile example/input/test.xml --destDir example/output
	bin/ipxact2c --srcFile example/input/test.xml --destDir example/output
	rst2html5.py example/output/example.rst example/output/example.html
	pandoc -s example/output/example.rst -o example/output/example.rtf
	pandoc -s example/output/example.rst -o example/output/example.docx

        # default config
	bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	bin/ipxact2md --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	bin/ipxact2c --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini

        # no default config
	bin/ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	bin/ipxact2rst --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	bin/ipxact2md --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	bin/ipxact2vhdl --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	bin/ipxact2c --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini

        #  test
	bin/ipxact2systemverilog --srcFile example/input/test2.xml --destDir example/output
	bin/ipxact2rst --srcFile example/input/test2.xml --destDir example/output
	bin/ipxact2md --srcFile example/input/test2.xml --destDir example/output
	bin/ipxact2vhdl --srcFile example/input/test2.xml --destDir example/output
	bin/ipxact2md --srcFile example/input/test2.xml --destDir example/output
	bin/ipxact2c --srcFile example/input/test2.xml --destDir example/output

compile: 
	test -d work || vlib work
	vlog  +incdir+example/output  example/output/example_sv_pkg.sv example/tb/sv_dut.sv example/tb/tb.sv
	vcom -93 example/output/*.vhd example/tb/vhd_dut.vhd
	vmake work > vmakefile

compile_ghdl:
	ghdl -a example/output/*.vhd example/tb/vhd_dut.vhd
	ghdl -e vhd_dut
	ghdl -r vhd_dut

test_c:
	gcc -Wall -g  example/test/example.c -o example.exe
	./example.exe

compile_verilator:
	verilator --cc example/output/example_sv_pkg.sv
	verilator --cc example/output_default/example_sv_pkg.sv
	verilator --cc example/output_no_default/example_sv_pkg.sv
	verilator --cc example/output/example2_sv_pkg.sv

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
	xmllint --noout --schema ipxact2systemverilog/xml/component.xsd  example/input/test2.xml

test_rst:
	rst-lint example/output/*.rst

venv: requirements.txt
	python3 -m venv ./venv
	pip install wheel
	python3 setup.py bdist_wheel 
	pip install --upgrade -r requirements.txt
