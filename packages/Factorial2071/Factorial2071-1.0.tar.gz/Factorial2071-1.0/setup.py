from setuptools import setup,find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'Factorial Value Calculator'
LONG_DESCRIPTION = 'You can get factorial value easly with this module. You need to do only import the module and call it and print it.'

setup(name='Factorial2071',
      version=VERSION,
      author='A.M.Hasith Samoddya',
      author_email='animatoon2007@gmail.com',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=find_packages(),
      install_requires=[],
      keywords=['python','factorial'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Unix"
          ])
