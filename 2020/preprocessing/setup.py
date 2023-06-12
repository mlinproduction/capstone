from setuptools import setup

setup(
    name='preprocessing',
    version='1.0',
    description='NLP preprocessing',
    author='DS in Prod',
    install_requires=[
        'numpy >=1.16.0, <2.0',
        'tensorflow >= 2.0, < 3',
        'transformers == 4.30.0',
        'scikit-learn >= 0.22, < 1.0',
        'pandas >=1.0.1, < 1.1'
    ]
)