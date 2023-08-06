"""Installation script for the nn_helper package."""
from pathlib import Path

from setuptools import find_packages, setup

THIS_DIRECTORY = Path(__file__).parent

VERSION = "1.1.1"
DESCRIPTION = "Neural network helper for Pytorch."
LONG_DESCRIPTION = (THIS_DIRECTORY / "README.md").read_text()

test = ["coverage>=6.0.2", "pre-commit>=2.15.0"]


setup(
    name="nn_helper",
    version=VERSION,
    license="MIT",
    author="Mark de Blaauw",
    author_email="markdeblaauw@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/markdeblaauw/nn-helper",
    packages=find_packages(include=["nn_helper", "nn_helper.*"]),
    install_requires=["torch>=1.9.1", "numpy>=1.21.2"],
    extras_require={
        "dev": test,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["python", "neural network", "pytorch"],
    python_requires=">=3.8",
)
