import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Snehil-101903064",
    version="2.0.0",
    description="Implements topsis on the given input data file and generates topsis score and ranks accordingly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Snehil-21/Topsis-Snehil-101903064",
    author="Snehil Gupta",
    author_email="sgupta2_be19@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)