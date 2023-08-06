from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'TOPSIS score calculation'
# LONG_DESCRIPTION = 'Performing TOPSIS using weights and impacts'

# Setting up
setup(
    name="Topsis-Jatin-101903431",
    version=VERSION,
    author="Jatin Goyal",
    author_email="<jg.silenttears.0786@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['topsispy', 'numpy', 'pandas'],
    keywords=['python','topsis','weight','socket'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)