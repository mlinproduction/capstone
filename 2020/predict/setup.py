from setuptools import setup
import os

setup(
    name='predict',
    version='1.0',
    description='Model Training',
    author='DS in Prod',
    install_requires=[
        'flask',
        'numpy >=1.16.0, <2.0',
        'tensorflow >= 2.0, < 3',
    ]
)