#!/usr/bin/env python

from setuptools import setup
from setuptools import find_namespace_packages

# Load the README file.
# with open(file="README.md", mode="r") as readme_handle:
#     long_description = readme_handle.read()

setup(
    name="pain-maker",  # Define the library name, this is what is used along with `pip install`.

    author="Daniel Jeon",
    # author_email="",

    # Define the version of this library.
    # Read this as
    #   - MAJOR VERSION 0
    #   - MINOR VERSION 1
    #   - MAINTENANCE VERSION 0
    version="0.1.0",

    # url="",  # GitHub repo link

    # Here's a small description of the library. This appears when the library is searched on https://pypi.org/search.
    description="A python program used to make the Pain Uni Schedules for each term/semester at OTU/UOIT",
    # long_description=long_description,  # using the README file, variable up above.

    long_description_content_type="text/markdown",  # This will specify that the long description is MARKDOWN.

    # Dependencies the library needs in order to run.
    install_requires=[
        "Pillow",
        "discord",
        "SQLAlchemy",
        "mysql-connector-python"
    ],

    # Here are the packages I want build.
    packages=find_namespace_packages(
        where=["ClassStructure", "JSONCourses", "JSONCourses.*", "JSONMaxTemplates", "Optimizations", "PNGMaker",
               "PNGMaker.*", "Scraper", "DB"]
    ),

    # This program requires some package data, such as font files, so include them
    include_package_data=True,

    # mysql connector for python requires python 3.7 if I remember correctly
    python_requires=">=3.7",

    # Characteristics about the package. (https://pypi.org/classifiers/)
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",

        "Natural Language :: English",

        "Operating System :: OS Independent",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",

        "Topic :: Database",
        "Topic :: Education"
    ]
)
