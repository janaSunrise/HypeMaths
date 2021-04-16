import re
from pathlib import Path

import setuptools

# Files
BASE_DIR = Path(__file__).resolve().parent

README = Path(BASE_DIR / "README.md").read_text()

# Constants
VERSION = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    Path(BASE_DIR / "hypemaths/__init__.py").read_text(),
    re.MULTILINE
).group(1)

URL = "https://github.com/Deep-Alchemy/HypeMaths"

if not VERSION:
    raise RuntimeError("VERSION is not set!")

# Setup
setuptools.setup(
    name="HypeMaths",
    version=VERSION,

    author="Deep Alchemy team",
    author_email="warriordefenderz@gmail.com",

    description="An extensible and easy way for advanced maths and its implementation in Python!",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GPL v3",

    url=URL,
    project_urls={
        "Documentation": URL,
        "Issue tracker": f"{URL}/issues",
    },

    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "tools", "tools.*"]
    ),
    install_requires=[],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",

        "Development Status :: 2 - Pre-Alpha",

        "Programming Language :: Python :: Implementation :: CPython",


        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: OS Independent",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Topic :: Scientific/Engineering :: Mathematics",

        "Natural Language :: English",
    ],

    python_requires=">=3.6",
)
