#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
#                                                        #
#   ██████╗ ██████╗  █████╗ ██╗  ██╗███████╗███╗   ██╗   #
#   ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║   #
#   ██║  ██║██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║   #
#   ██║  ██║██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║   #
#   ██████╔╝██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║   #
#   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   #
#                                                        #
#                Copyright © 2022 Draken TT              #
#                   https://draken.ee                    #
#                                                        #
##########################################################

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
      name='JsoNomads',
      version='1.0.3',
      license='GPLv3',
      description='Download nomads data from NOAA and convert the grib file to JSON',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      author='Draken TT',
      author_email='info@draken.ee',
      url='https://draken.ee',
      packages=['jsonomads'],
      install_requires=[
        "attrs>=21.4.0",
        "cffi>=1.15.0",
        "cfgrib>=0.9.10.0",
        "click>=8.0.3",
        "eccodes>=1.4.0",
        "ecmwflibs>=0.4.6",
        "findlibs>=0.0.2",
        "importlib-metadata>=4.11.1",
        "numpy>=1.21.5",
        "pandas>=1.3.5",
        "pycparser>=2.21",
        "python-dateutil>=2.8.2",
        "pytz>=2021.3",
        "six>=1.16.0",
        "typing_extensions>=4.1.1",
        "xarray>=0.20.2",
        "zipp>=3.7.0",
      ],
      entry_points = {
              'console_scripts': ['jsonomads=jsonomads:main'],
      },
      classifiers=[
              'Development Status :: 5 - Production/Stable',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Topic :: Scientific/Engineering :: Atmospheric Science',
              'Topic :: Software Development :: Libraries :: Python Modules'
              ],
)
