from setuptools import setup, find_packages

# Load the README file
with open("README.md", mode="r") as _file:
    long_description = _file.read()

setup(
    name='GrandExchangeToolbox',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy",
        "fuzzywuzzy",
        "matplotlib",
        "pyyaml",
        "pydantic",
    ],
    url='https://github.com/Lee-Tyrer/GrandExchange-ToolBox',
    license='',
    author='Lee',
    author_email='lee.4lifee@gmail.com',
    description='A package to interact with the Grand Exchange',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
