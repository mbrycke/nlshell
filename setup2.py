# setup.py
from setuptools import setup, find_packages

setup(
    name='command-geni',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'c=main:main',
        ],
    },
    install_requires=[
        'openai>=1.52.2',
    ]
)