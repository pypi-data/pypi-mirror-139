from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.0.0'
DESCRIPTION = 'i8.ae python library'

# Setting up
setup(
    name="i8.ae",
    version=VERSION,
    author="ShahabCypher (Shahab Cypher)",
    author_email="<shahabcypher@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'i8.ae', 'i8.ae Python', 'i8.ae api', 'python link shortener', 'py link shortener', 'py i8.ae', 'pypi i8', 'pypi i8.ae'],
    classifiers=[
	    "Development Status :: 5 - Production/Stable",
	    "Intended Audience :: Developers",
	    "Programming Language :: Python :: 3",
	    "Operating System :: OS Independent",
    ]
)