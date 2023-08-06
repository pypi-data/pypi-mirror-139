import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="minicalculator",
    version="0.1.0",
    description="A basic Calculator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Idris01/calculator",
    author="Idris Adebowale",
    author_email="idrys01@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["mini_calculator"],
    include_package_data=True,
    
    
)