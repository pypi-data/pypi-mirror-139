from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
install_requires = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="pvoutput-ocf",
    version="0.1.3",
    packages=find_packages(),
    install_requires=install_requires,
)
