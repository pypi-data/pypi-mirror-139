import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


REPO_URL = "https://github.com/notjawad/wmapi"

setup(
    name="weedmaps",
    version="0.2.4",
    author="Jawad A",
    author_email="imjawad73@yahoo.com",
    description="The Unofficial Weedmaps API Wrapper",
    license="MIT",
    keywords=["weedmaps", "weed", "weed api", "cannabis", "marijuana"],
    url=REPO_URL,
    install_packages=["httpx"],
    long_description=read('README.md'),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
