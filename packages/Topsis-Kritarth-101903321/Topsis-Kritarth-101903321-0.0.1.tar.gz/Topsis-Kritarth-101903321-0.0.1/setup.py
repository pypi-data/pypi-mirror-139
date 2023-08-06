from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Topsis Package by Kritarth Gupta'

# Setting up
setup(
    name="Topsis-Kritarth-101903321",
    version=VERSION,
    author="Kritarth Gupta",
    author_email="<kgupta1_be19@thapar.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy','sys'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
