from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='ipxact2systemverilog',
      python_requires='>=3',
      version='1.0.12',
      description='Generate VHDL, SystemVerilog, html, rst, md, pdf from an IPXACT description',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='ipxact2systemverilog ipxact2vhdl VHDL SystemVerilog html rst md pdf IPXACT',
      url='https://github.com/oddball/ipxact2systemverilog',
      author='oddball',
      license='GPL',
      packages=['ipxact2systemverilog'],
      install_requires=requirements,
      scripts=['bin/ipxact2rst', 'bin/ipxact2md', 'bin/ipxact2systemverilog', 'bin/ipxact2vhdl'],
      include_package_data=True,
      zip_safe=False)
