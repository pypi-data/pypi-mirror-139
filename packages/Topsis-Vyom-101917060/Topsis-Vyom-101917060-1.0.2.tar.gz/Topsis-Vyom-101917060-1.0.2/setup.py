import os
from setuptools import setup

NAME = "Topsis-Vyom-101917060"
VERSION = "1.0.2"
DESCRIPTION = "A package for topsis score generation in mere moments"
AUTHOR = "Vyom Chopra"
AUTHOR_EMAIL = "vchops652000@gmail.com"
PACKAGES_PRESENT = ['Topsis-Vyom-101917060']
PACKAGES_NEED = ['pandas','numpy']

def read_file(name):
    path = os.getcwd()
    return open(f"{path}\{name}").read()

setup(
    name = NAME,
    version = VERSION,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    description = DESCRIPTION,
    packages = PACKAGES_PRESENT,
    install_requires = PACKAGES_NEED,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license = read_file('LICENSE.txt')
)

