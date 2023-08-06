import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="koltk", 
    version="0.1.0",
    author="",
    author_email="",
    description="Korean Language Toolkit",
    long_description="README.rst",
    url="https://github.com/koltk/koltk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
