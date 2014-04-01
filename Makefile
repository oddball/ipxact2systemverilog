
ifneq ($(wildcard vmakefile),)
include vmakefile
endif

XSD_DIR = schema1.5

all: gen

gen: validate
	bin/ipxact2systemverilog.py --srcFile input/test.xml --destDir output
	bin/ipxact2rst.py --srcFile input/test.xml --destDir output
	bin/ipxact2vhdl.py --srcFile input/test.xml --destDir output
	rst2html output/example.rst output/example.html
	rst2pdf output/example.rst -o output/example.pdf
	rst2pdf README.rst -o README.pdf

compile: 
	test -d work || vlib work
	vlog  +incdir+output  output/example_sv_pkg.sv tb/sv_dut.sv tb/tb.sv
	vcom -93 output/*.vhd tb/vhd_dut.vhd
	vmake work > vmakefile

xmlschema:
	test -d ${XSD_DIR} || mkdir ${XSD_DIR}
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/component.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/busInterface.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/identifier.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/memoryMap.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/file.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/commonStructures.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/autoConfigure.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/configurable.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/simpleTypes.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/fileType.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/port.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/constraints.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/signalDrivers.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/generator.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/model.xsd
	wget --quiet --directory-prefix=${XSD_DIR} http://www.accellera.org/XMLSchema/SPIRIT/1.5/subInstances.xsd

	@echo "Set the env. variable 'ipxactRoot' to use the local XML Schema"
	@echo "e.g.: export ipxactRoot=${XSD_DIR}"

validate:
ifeq ($(ipxactRoot),)
	@echo "Please download the xsd files, and use local files for faster validation"
	xmllint --noout --schema http://www.accellera.org/XMLSchema/SPIRIT/1.5/component.xsd input/test.xml
else
	xmllint --noout --schema $(ipxactRoot)/${XSD_DIR}/component.xsd  input/test.xml
endif


.PHONY: whole_library output

sim: whole_library
	vsim tb -c -do "run -all; quit -force"

gui: whole_library
	vsim tb -voptargs="+acc" -debugDB -do "add log -r /*; run -all;"

indent:
	emacs -batch -l ~/.emacs output/*.sv tb/*.sv -f verilog-batch-indent
	emacs -batch -l ~/.emacs output/*.vhd -f vhdl-beautify-buffer

clean:
	rm -rf work transcript vsim.wlf vmakefile vsim.dbg output/*


pep8:
	pep8 bin/*.py


autopep8:
	autopep8 --max-line-length 120 --in-place bin/*.py
