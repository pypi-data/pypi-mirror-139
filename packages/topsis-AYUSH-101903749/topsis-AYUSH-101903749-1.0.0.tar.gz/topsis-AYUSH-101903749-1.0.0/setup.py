import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="topsis-AYUSH-101903749",
    version="1.0.0",
    description="Multiple criteria decision making (MCDM) using TOPSIS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gayush2510/Topsis",
    author="Ayush Goyal",
    author_email="gayush2510@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["Topsis-Ayush-101903749"],
    include_package_data=True,
    install_requires=[],
)