from setuptools import setup, find_packages

import subprocess as sp
import os
import sys
import shutil

version_file = "package_version.txt"
dll_extensions = ["dll", "so"]
python_package_dir = "_python_package"

def get_os():
    from sys import platform

    if platform == "linux" or platform == "linux2":
        return "linux"

    elif platform == "darwin":
        return "osx"

    elif platform == "win32":
        return "win"

def get_dll_ext():
    return "dll" if get_os() == "win" else "so"

def get_long_description():
    print(f"{os.getcwd()=}")
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    return long_description

def get_version():
    print(f"{os.getcwd()=}")
    with open(version_file, "r") as f:
        version = f.read().strip()
    return version

long_description = get_long_description()
version = get_version()

setup(
    name="light_labyrinth",
    version=version,
    author="Marcin Zakrzewski, Krzysztof Wieclaw",
    author_email="enkar@lightlabyrinth.org, wutus@lightlabyrinth.org",
    description="Light labyrinth ML model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lightlabyrinth.org",
    project_urls={
        "Source Code": "https://bitbucket.org/Enkar234/lightlabyrinth",
        "Documentation": "https://lightlabyrinth.org", 
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    py_modules=["light_labyrinth", "light_labyrinth._light_labyrinth_c"],
    package_dir={"": python_package_dir},
    packages=find_packages(python_package_dir),
    python_requires=">=3.8",
    include_package_data=True,
    package_data={"light_labyrinth._light_labyrinth_c": [f"light_labyrinth.{x}" for x in dll_extensions]},
    install_requires=["scikit-learn", "numpy"]
)
