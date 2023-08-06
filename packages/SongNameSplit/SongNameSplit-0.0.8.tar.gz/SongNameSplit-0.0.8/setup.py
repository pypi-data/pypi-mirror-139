from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.8'
DESCRIPTION = 'Seperate the song and artist name from a song title'
LONG_DESCRIPTION = 'Seperate the song and artist name from a song title. This is still under development.'

setup(
    name="SongNameSplit",
    version=VERSION,
    author="Archit Tandon",
    author_email="archittandon26@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['google', 'bs4', 'requests', 'beautifulsoup4'],
    keywords=['python', 'song', 'artist name', 'song name'],
    classifiers=[]
)
