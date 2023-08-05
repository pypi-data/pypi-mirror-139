import setuptools
from pathlib import Path

setuptools.setup(
    name="pypam3",
    version='0.1.0',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/plain',
    packages=setuptools.find_packages(exclude=["tests", "data", "venv"])
)
