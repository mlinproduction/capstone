from setuptools import setup

setup(
    name='preprocessing',
    description='NLP preprocessing',
    author='DS in Prod',
    install_requires=[
        'numpy >=1.16.0, <2.0',
        'tensorflow >= 2.0, < 3',
        'transformers == 2.4.1',
        'scikit-learn >= 0.22, < 1.0',
        'pandas >=1.0.1, < 1.1'
    ],
    use_scm_version=True
)