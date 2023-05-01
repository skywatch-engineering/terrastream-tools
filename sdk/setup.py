from os import path
from shutil import rmtree

from setuptools import setup

module_name = "ts_sdk"


def cleanup(name):
    if path.exists("dist"):
        rmtree("dist")
    if path.exists("build"):
        rmtree("build")
    if path.exists(f"{name}.egg-info"):
        rmtree(f"{name}.egg-info")


cleanup(module_name)


setup(
    name=module_name,  # This is the name of your PyPI-package.
    version="0.4.1",  # Update the version number for new releases
    description="TS software development kit",
    url="https://github.com/skywatch-engineering/terrastream-tools.git",
    author="SkyWatch Engineering",
    author_email="team@skywatch.com",
    license="Private",
    packages=[
        f"{module_name}",
        f"{module_name}.api",
        f"{module_name}.api.endpoints",
        f"{module_name}.models",
        f"{module_name}.models.api",
        f"{module_name}.models.api.generated",
        f"{module_name}.mappers",
        f"{module_name}.controllers",
        f"{module_name}.wrappers",
    ],
    install_requires=["requests"],
    python_requires=">=3.9",
)
