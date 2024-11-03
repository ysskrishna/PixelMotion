from setuptools import setup, find_packages
from pm_common import __version__

setup(
    name="pm_common",
    description="Common utilities for Pixelmotion",
    author="ysskrishna",
    version=__version__,
    packages=find_packages(where=".", include=["pm_common", "pm_common.*"]),
    python_requires=">=3.10",
    install_requires=[
        "redis",
        "boto3",
        "rq"
    ],
)