from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

this_directory = Path(__file__).parent
#VERSION = '0.0.1'
DESCRIPTION = 'TOPSIS Implementation using Python'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
# Setting up
setup(
    name="Topsis_Shikha_101903629",
    version=None,
    author="ShikhaShikha",
    author_email="sshikha_be19@thapar.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'topsis python', 'calculate topsis score', 'TOPSIS', 'topsis using python',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)