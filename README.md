# ipxact2systemverilog ipxact2rst ipxact2md ipxact2vhdl ipxact2c ipxact2py

[![CI](https://github.com/oddball/ipxact2systemverilog/actions/workflows/ci.yml/badge.svg)](https://github.com/oddball/ipxact2systemverilog/actions/workflows/ci.yml)

[![image](https://badge.fury.io/py/ipxact2systemverilog.svg)](https://pypi.python.org/pypi/ipxact2systemverilog/)

This software takes an IP-XACT description of register banks, and
generates synthesizable VHDL and SystemVerilog packages and
ReStructuredText documents. It ONLY considers register bank
descriptions. The software does not generate OVM or UVM test bench
packages. In the example/tb directory there is an example of how to use
the generated packages.

## Usage

```bash
pip install ipxact2systemverilog

ipxact2systemverilog --srcFile FILE --destDir DIR
ipxact2rst --srcFile FILE --destDir DIR
ipxact2md --srcFile FILE --destDir DIR
ipxact2vhdl --srcFile FILE --destDir DIR
ipxact2c --srcFile FILE --destDir DIR
ipxact2py --srcFile FILE --destDir DIR
```

## Development

See https://github.com/oddball/ipxact2systemverilog

```bash
python -m venv venv
source venv/bin/activate
pip install build
python -m build
python -m pip install .
# In order to publish:
pip install twine
twine upload dist/*
```

## Testing the example file

```bash
make
```

If Modelsim is installed: :

```bash
make compile
make sim
```

## Note

You can use <http://pandoc.org/demos.html> to convert to almost any
fileformat.

## Validation

To validate your xml :

```bash
xmllint --noout --schema ipxact2systemverilog/xml/component.xsd  example/input/test.xml
```

## Dependencies

```bash
pip install docutils lxml mdutils
```

## Dependencies used by makefile

These are not needed for ipxact2systemverilog, but used for generating
some of the files in example/output. Instructions are for MacOsX, similiar packages are
available for Linux and Windows.

```bash
brew install pandoc verilator ghdl

# if you want to use sphinx
brew install texlive
sudo tlmgr install latexmk
```

## TODO

- A better test bench for the generated packages should be implemented.
- More complicated IPXACT files should be added and tried out.
- Add support for the SystemVerilog generator to have a register field
  of an enumerated type.
- Support DIM
- Eat some cheese and drink some wine 2024-06-20
