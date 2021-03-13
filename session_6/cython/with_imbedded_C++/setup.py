#!/usr/bin/env python3

from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize("matrix.pyx", compiler_directives={'language_level' : "3"}, annotate=True))
