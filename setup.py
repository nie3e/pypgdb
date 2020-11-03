import setuptools
import os


def get_version(version_tuple):
    return ".".join(map(str, version_tuple))


init = os.path.join(
    os.path.dirname(__file__), "pypgdb/__init__.py"
)

version_line = list(
    filter(lambda l: l.startswith("VERSION"), open(init))
)[0]

VERSION = get_version(eval(version_line.split("=")[-1]))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypgdb",
    version=VERSION,
    description="A wrapper around psycopg2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adrian Ćwiek",
    author_email="adrcwiek@gmail.com",
    install_requires=[
        "psycopg2>=2.8.3"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Database"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    url="https://github.com/nie3e/pypgdb"
)
