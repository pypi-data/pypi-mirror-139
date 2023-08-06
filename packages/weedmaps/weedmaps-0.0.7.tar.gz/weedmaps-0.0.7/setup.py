import os

from setuptools import find_packages, setup

__version__ = "0.0.7"


with open(os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "README.md")
) as f:
    README = f.read()

repo_url = "https://github.com/notjawad/wmapi"
setup(
    version=__version__,
    name="weedmaps",
    packages=find_packages(),
    install_requires=["httpx"],
    description="The Unofficial Weedmaps API wrapper",
    long_description=README,
    author="NotJawad",
    author_email="imjawad73@yahoo.com",
    url=repo_url,
    download_url=f"{repo_url}/archive/{__version__}.tar.gz",
    license="GPLv3 License",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
