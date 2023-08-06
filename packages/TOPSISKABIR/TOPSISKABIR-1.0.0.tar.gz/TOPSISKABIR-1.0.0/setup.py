from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'Topsis Calculation using weights and impacts'

# Setting up
setup(
    name="TOPSISKABIR",
    version=VERSION,
    author="Kabir Chhabra",
    author_email="<kabir12chhabra@gmail.com>", 
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['topsispy', 'numpy', 'pandas'],
    keywords=['python', 'topsis', 'topsis_rank', 'weights', 'impacts'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)