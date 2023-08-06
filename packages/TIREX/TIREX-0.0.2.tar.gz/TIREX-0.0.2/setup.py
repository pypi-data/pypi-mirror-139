from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path


this_directory = Path(__file__).parent



VERSION = '0.0.2'
DESCRIPTION = 'Dimensionality Reduction in extreme regions'
long_description = (this_directory / "README.md").read_text()
# Setting up
setup(
    name="TIREX",
    version=VERSION,
    author="Anass Aghbalou",
    author_email="anass.aghbalou@hotmail.com",

    description=DESCRIPTION,
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['scikit-learn'],
    keywords=['python', 'Dimensionality reduction', 'Large/extreme values', 'Machine learning','regression','anomaly detection'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
