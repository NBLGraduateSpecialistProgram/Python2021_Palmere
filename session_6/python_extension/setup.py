#!/usr/bin/env python3

import os
from setuptools import setup, Extension

module = Extension('matrix', sources=['matrixmodule.cpp'], language='c++')

setup(name='matrix', ext_modules = [module])


