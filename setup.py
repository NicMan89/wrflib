import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='v1',
    version='0.0.1',
    description='',
    url='#',
    author='Nicola Manconi',
    author_email='nicolamanconi8@gmail.com',
    license='MIT',
    install_requires=required,
    packages=find_packages(include=['WRFLIB','WRFLIB.*']),
    zip_safe=False
)
#pipreqs /home/project/location