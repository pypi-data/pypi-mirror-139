import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="clusterInterface",
    version="0.0.1",
    author="Intelligent Ultrasound",
    author_email="laurence.still@intelligentultrasound.com",
    packages=[],
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3"
    ]
)


