from setuptools import setup, find_packages
from pathlib import Path

with open(Path(__file__).joinpath("../README.md").resolve()) as file:
    long_description = file.read()

setup(
    name='spt_gfx',
    author='Sindre T. Strøm',
    version="1.0.0",
    url='https://github.com/sindrets/spt_gfx',
    description='A simple, lightweight framework for creating graphics in the terminal.',
    long_description=long_description,
    packages=find_packages(),
    python_requires='>=3.6'
)
