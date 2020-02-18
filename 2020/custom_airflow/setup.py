from setuptools import setup

setup(
    name='custom_airflow',
    version='1.0',
    description='Custom Airflow',
    author='DS in Prod',
    install_requires=[
        'apache-airflow[crypto,gcp]==1.10.7'
    ]
)