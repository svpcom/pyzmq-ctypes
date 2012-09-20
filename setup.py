#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2011 Daniel Holth
# 
# Derived from original pyzmq © 2010 Brian Granger
#
# This file is part of pyzmq-ctypes
#
# pyzmq-ctypes is free software; you can redistribute it and/or modify it
# under the terms of the Lesser GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# pyzmq-ctypes is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU General Public
# License for more details.
#
# You should have received a copy of the Lesser GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import os, sys

from distutils.core import setup

long_desc = \
"""
pyzmq-ctypes is a ctypes binding for the ZeroMQ library
(http://www.zeromq.org) that will run on pypy.
"""

setup(
    name = "pyzmq-ctypes",
    version = "2.1.9",
    packages = ['zmq', 'zmq.core'],
    author = "Daniel Holth",
    author_email = "dholth@fastmail.fm",
    url = 'http://github.com/svpcom/pyzmq-ctypes',
    download_url = 'http://python.org/pypi/pyzmq-ctypes',
    description = "Python bindings for 0MQ (ctypes version).",
    install_requires = ['ctypes_configure'],
    long_description = long_desc,
    license = "LGPL",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX',
        'Topic :: System :: Networking'
    ]
)

