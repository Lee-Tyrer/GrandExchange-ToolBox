from setuptools import setup
from setuptools import find_namespace_packages

# Load the README file
with open("README.md", mode="r") as _file:
    long_description = _file.read()

setup(
    name='GrandExchange-ToolBox',
    version='0.1',
    packages=find_namespace_packages("toolbox"),
    install_requires=[
        "requests",
        "pandas",
        "fuzzywuzzy",
        "matplotlib",
    ],
    url='https://github.com/Lee-Tyrer/GrandExchange-ToolBox',
    license='',
    author='Lee',
    author_email='lee.4lifee@gmail.com',
    description='A package to interact with the Grand Exchange',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
