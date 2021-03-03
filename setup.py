# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhermit", # Replace with your own username
    version="1.01",
    author="LookCos",
    author_email="lookcos@gmail.com",
    description="Hermit的python版接口，详细说明请看README.md",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LookCos/hermit-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU GENERAL PUBLIC LICENSE Version 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)