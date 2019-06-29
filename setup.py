import sys
import os

from setuptools import setup
from distutils.sysconfig import get_python_lib

version = "1.0.0a1"

SITE_PACKAGES_PATH = os.path.relpath(get_python_lib(), sys.prefix)

setup(
    name="pypreload",
    version=version,
    packages=["pypreload"],
    url="https://github.com/ConnorNelson/pypreload",
    description="LD_PRELOAD, but for Python.",
    author="Connor Nelson",
    data_files=[(SITE_PACKAGES_PATH, ['pypreload.pth'])]
)
