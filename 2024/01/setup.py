from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("main_cy.py", annotate=True))