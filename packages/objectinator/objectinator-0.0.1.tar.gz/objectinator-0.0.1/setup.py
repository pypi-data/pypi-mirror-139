from setuptools import setup

with open("README.md") as f:
    README = f.read()

setup(
    name = "objectinator",
    version="0.0.1",
    author= "Mike Zinyoni",
    author_email="mzinyoni7@outlook.com",
    description="Python packege to help navigate between dictionaries, tuples, lists, sets and object classes",
    long_description=README,
    packages=["objectinator"],
    requires=[],
    keywords=["Objects", "Lists", "Dictionaries", "Tuples"]
)