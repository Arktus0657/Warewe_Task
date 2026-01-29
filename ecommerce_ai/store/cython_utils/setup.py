# store/cython_utils/setup.py

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("store/cython_utils/scorer.pyx", language_level=3)
)
