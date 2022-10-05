"""
Setup module
"""
import sys
import os
from setuptools import find_packages, setup

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

with open("requirements.txt", encoding="utf-8") as file:
    required = file.read().splitlines()

setup(
    name="arvoitus-backend",
    version="0.0.1",
    author="Alexey Nikolaev",
    author_email="alexey.nikolaev@aaltoes.com",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
