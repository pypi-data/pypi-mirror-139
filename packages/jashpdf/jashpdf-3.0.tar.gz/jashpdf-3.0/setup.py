import setuptools
from pathlib import Path
setuptools.setup(
    name="jashpdf",
    version="3.0",
    long_description=Path("README.MD").read_text(),
    packages=setuptools.find_packages(exclude=["tests, data"])
)
