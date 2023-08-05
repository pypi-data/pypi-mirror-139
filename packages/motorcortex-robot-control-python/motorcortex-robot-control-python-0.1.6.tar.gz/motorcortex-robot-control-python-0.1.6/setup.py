#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2020 VECTIONEER.
#


from setuptools import setup
from robot_control.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('robot_control/version.py').read())
setup(name='motorcortex-robot-control-python',
      version=__version__,
      description='Python bindings for Motorcortex Robot Control',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Alexey Zakharov',
      author_email='info@vectioneer.com',
      url='https://www.motorcortex.io',
      license='MIT',
      packages=['robot_control'],
      install_requires=['motorcortex-python'],
      include_package_data=True, 
      )
