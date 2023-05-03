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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import os

from pydantic import BaseModel
from pydantic import Field


class ConfigModel(BaseModel):
    """
    {
        "name": "provider_name",
        "username": "foo",
        "password": "bar",
        "base_url": "https://api.provider.domain.com/api",
    }
    """

    name: str = Field(..., description="Terrastream account user name")
    username: str = Field(..., description="Terrastream account user name")
    password: str = Field(..., description="Terrastream account password")
    base_url: str = Field(..., description="Terrastream base account url")
