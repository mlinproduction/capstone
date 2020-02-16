from setuptools import setup

setup(
    name='train',
    description='Model Training',
    author='DS in Prod',
    install_requires=[
        'tensorflow >= 2.0, < 3',
        'preprocessing==1.0'
    ],
    use_scm_version=True
)