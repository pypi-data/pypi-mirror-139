#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="ColoraPy",
    author_email="tiktok.agn@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="wsp",
    install_requires=[],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"ColoraPy": ["py.typed"]},
    include_package_data=True,
    keywords="ColoraPy",
    name="ColoraPy",
    package_dir={"": "src"},
    packages=find_packages(include=["src/ColoraPy", "src/ColoraPy.*"]),
    setup_requires=[],
    url="https://github.com/YuxOnTop/ColoraPy",
    version="0.1.0",
    zip_safe=False,
)
