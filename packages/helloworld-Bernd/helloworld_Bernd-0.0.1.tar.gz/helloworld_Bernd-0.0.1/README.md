# Hello World

This is an example project demonstrating how publich a python module to PyPI

##Installation

Run the following to install:

'''python pip install helloworld_Bernd'''

##Usage

'''python 
from helloworld_Bernd import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")
'''

# Developing Hello World

To install helloworld_Bernd, aling with the tool you need to develop and run tests, run the following in you r virtualenv:

'''bash
$ pip install -e .[dev]
'''
