import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='wrflib',
    version='0.0.3',
    description='',
    url='https://github.com/NicMan89/wrflib',
    author='Nicola Manconi',
    author_email='nicolamanconi8@gmail.com',
    license='MIT',
    python_requires='>=3.6',
    install_requires=required,
    packages=find_packages(),
    zip_safe=False
)
#pipreqs /home/project/location
#include=['WRFLIB','WRFLIB.*']
