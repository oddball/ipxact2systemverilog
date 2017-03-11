from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='ipxact2systemverilog',
      version='0.1',
      description='Generate VHDL, SystemVerilog, html, rst, pdf from an IPXACT description',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='ipxact2systemverilog ipxact2vhdl VHDL SystemVerilog html rst pdf IPXACT',
      url='https://github.com/oddball/ipxact2systemverilog',
      author='oddball',
      license='GPL',
      packages=['ipxact2systemverilog'],
      install_requires=[
          'docutils', 'rst2pdf', 'lxml'
      ],
      scripts=['ipxact2rst', 'ipxact2systemverilog', 'ipxact2vhdl']
      include_package_data=True,
      zip_safe=False)
