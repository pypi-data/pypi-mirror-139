from pathlib import Path
from setuptools import setup, find_packages
import os
os.chdir(os.getcwd())

with open("/Users/jamell/code/languages/python/primepackage/readme.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="primepackage",
    version="1.1.6",
    description="A prime package for calculating prime numbers and non trivial riemann zeros",
    keywords="prime, riemann, maths, calculation, numerical",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamellknows/primepackage",
    author="jamellknows",
    author_email="jamellsamuels@googlemail.com",
    license="MIT",
    packages = find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    py_modules=["isprime", "isriemann", "randomprime", "primelist", "riemannlist"],
    python_requires='>=3.6',
    package_dir={"src":"src"},

   
)