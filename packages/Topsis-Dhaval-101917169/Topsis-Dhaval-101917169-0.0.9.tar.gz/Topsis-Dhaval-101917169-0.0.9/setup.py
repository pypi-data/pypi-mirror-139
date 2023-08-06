from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
DESCRIPTION = 'Topsis program'
LONG_DESCRIPTION = 'Topsis package that allows to calculate topsis score. Give command as pip install Topsis-Dhaval-101917169. Give input csv file name, impacts, weights, output csv file name.'

# Setting up
setup(
    name="Topsis-Dhaval-101917169",
    version=VERSION,
    author="Dhaval Arya",
    author_email="arya.dhavalv@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
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