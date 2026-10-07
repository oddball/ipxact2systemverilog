ifneq ($(wildcard vmakefile),)
include vmakefile
endif

XSD_DIR = schema1.5


all: gen

gen:
	# no config
	ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output
	ipxact2rst --srcFile example/input/test.xml --destDir example/output
	ipxact2md --srcFile example/input/test.xml --destDir example/output
	ipxact2vhdl --srcFile example/input/test.xml --destDir example/output
	ipxact2md --srcFile example/input/test.xml --destDir example/output
	ipxact2c --srcFile example/input/test.xml --destDir example/output
	ipxact2py --srcFile example/input/test.xml --destDir example/output
	pandoc -s example/output/example.rst -o example/output/example.html
	pandoc -s example/output/example.rst -o example/output/example.rtf
	pandoc -s example/output/example.rst -o example/output/example.pdf

	# 2022
	ipxact2systemverilog --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2rst --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2md --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2vhdl --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2md --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2c --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	ipxact2py --xmlVersion 2022 --srcFile example/input/test_2022.xml --destDir example/output_2022
	pandoc -s example/output_2022/example.rst -o example/output_2022/example.html
	pandoc -s example/output_2022/example.rst -o example/output_2022/example.rtf
	pandoc -s example/output_2022/example.rst -o example/output_2022/example.pdf

        # default config
	ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	ipxact2rst --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	ipxact2md --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	ipxact2vhdl --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	ipxact2c --srcFile example/input/test.xml --destDir example/output_default  --config example/input/default.ini
	ipxact2py --srcFile example/input/test.xml --destDir example/output_default -- config example/input/default.ini

        # no default config
	ipxact2systemverilog --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	ipxact2rst --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	ipxact2md --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	ipxact2vhdl --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	ipxact2c --srcFile example/input/test.xml --destDir example/output_no_default  --config example/input/no_default.ini
	ipxact2py --srcFile example/input/test.xml --destDir example/output_no_default --config example/input/no_default.ini

	# RestructuredText and Sphinx with Wavedrom
	ipxact2rst --srcFile example/input/test.xml --destDir example/output_sphinx --config example/input/sphinx.ini
	sphinx-build example/output_sphinx example/output_sphinx/build -q -b latex
	make -C example/output_sphinx/build
	cp example/output_sphinx/build/example.pdf example/output_sphinx

	#  test2
	ipxact2systemverilog --srcFile example/input/test2.xml --destDir example/output
	ipxact2rst --srcFile example/input/test2.xml --destDir example/output
	ipxact2md --srcFile example/input/test2.xml --destDir example/output
	ipxact2vhdl --srcFile example/input/test2.xml --destDir example/output
	ipxact2md --srcFile example/input/test2.xml --destDir example/output
	ipxact2c --srcFile example/input/test2.xml --destDir example/output
	ipxact2py --srcFile example/input/test.xml --destDir example/output


compile:
	test -d work || vlib work
	vlog  +incdir+example/output  example/output/example_sv_pkg.sv example/tb/sv_dut.sv example/tb/tb.sv
	vcom -93 example/output/*.vhd example/tb/vhd_dut.vhd
	vmake work > vmakefile

compile_ghdl:
	ghdl -a --std=08 example/output/*.vhd example/tb/*.vhd
	ghdl -e --std=08 tb_vhd
	ghdl -r --std=08 tb_vhd

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

.PHONY: whole_library example/output test_2022 venv

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
	rm -rf a.out tb_sim obj_dir tb_icarus_sim tb_pkg_sim tb_sv_sim

validate:
	xmllint --noout --schema ipxact2systemverilog/xml/ipxact-1.5/component.xsd  example/input/test.xml
	xmllint --noout --schema ipxact2systemverilog/xml/ipxact-1.5/component.xsd  example/input/test2.xml
	xmllint --noout --schema ipxact2systemverilog/xml/ieee-1685-2022/component.xsd  example/input/test_2022.xml

test_rst:
	rst-lint example/output/example.rst  # example2.rst does have an error when not usign Sphinx
	rst-lint example/output_default/*.rst
	rst-lint example/output_no_default/*.rst

test_py:
	pylint example/output/*.py
	pylint example/output_default/*.py
	pylint example/output_no_default/*.py

venv:
	python3 -m venv ./venv
	./venv/bin/pip install -e ".[dev]"
