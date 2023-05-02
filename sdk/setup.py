# Copyright 2023 Skywatch Space Applciations Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from os import path
from shutil import rmtree

from setuptools import setup

module_name = "ts_sdk"

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
