import argparse
import os
from setuptools import find_packages, setup

with open('lib/requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name=f"pypescript_interface",
    packages=find_packages(include=['lib']),
    version=f"0.0.2",
    install_requires=required,
    description='Pypescript Interfaces. Typescript style Interface lib, for strongly typing objects in python',
    url='https://github.com/gitnology/Pypescript-Interfaces',
    author='Electric Sheep',
    license='MIT',
)